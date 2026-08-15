#!/usr/bin/env python3
"""Full pipeline A/B: with-facets vs skip-facets (CERA locked CQAs → CGR → CBTE → Aggregate).

Uses corrected CERA CQAs (no re-extraction) so the only arm difference is CGR facets.
Students = first N from student_smoke_n10. Gold = SAF human marks.

Usage (from scales_v3/):
  .venv/bin/python scripts/run_full_pipeline_facets_ab.py
  .venv/bin/python scripts/run_full_pipeline_facets_ab.py --qids CE04 CE08 --n 8
  .venv/bin/python scripts/run_full_pipeline_facets_ab.py --no-nli   # faster, no entailment
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import shutil
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from scales.config import get_settings
from scales.models.cqa import CQATuple
from scales.models.exam import ExamInput, QuestionInput, StudentAnswer
from scales.models.trust import TrustDecision
from scales.persistence import ExamStore
from scales.pipeline import GradingPipeline
from scales.services.llm_client import LLMClient
from scales.services.nli_service import NLIService

PROJECT = Path(__file__).resolve().parents[1]
CORRECTED = PROJECT / "data/cera_eval/runs/cera_eval_v1_corrected"
SMOKE = PROJECT / "data/cera_eval/runs/student_smoke_n10"
OUT = PROJECT / "data/cera_eval/runs/full_pipeline_facets_ab"
EXAMS_ROOT = OUT / "exams"
CACHE = (
    Path.home()
    / ".cache/huggingface/hub/datasets--Meyerger--ASAG2024"
    / "snapshots/9a7a179de4e227f5e78625bc9ded2d8761f1ff09/train.parquet"
)
LOCAL = {
    "CE01": PROJECT
    / "data/e2e_eval/wave5_real/saf_wave6_picked/wave6_coarse_n20/dll_service_classes/source.parquet",
    "CE04": PROJECT
    / "data/e2e_eval/wave5_real/saf_wave6_picked/wave6_coarse_n20/frame_bursting/source.parquet",
}
DEFAULT_QIDS = ["CE04", "CE08", "CE03", "CE07", "CE01", "CE06", "CE10"]


def load_pool(qid: str, qtext: str, saf: pd.DataFrame | None) -> pd.DataFrame:
    if qid in LOCAL and LOCAL[qid].exists():
        return pd.read_parquet(LOCAL[qid])
    assert saf is not None
    key = re.sub(r"\s+", " ", qtext)
    for n in (50, 35, 25):
        m = saf[saf["question"].astype(str).str.contains(re.escape(key[:n]), case=False, na=False)]
        if len(m) >= 5:
            return m
    words = re.findall(r"[A-Za-z]{4,}", qtext)[:6]
    return saf[
        saf["question"]
        .astype(str)
        .str.contains(".*".join(words[:4]), case=False, na=False, regex=True)
    ]


def match_ans(pool: pd.DataFrame, preview: str):
    hits = pool[pool["provided_answer"].astype(str).str.startswith(preview[:50].rstrip(), na=False)]
    if len(hits) == 0:
        key = re.sub(r"\s+", " ", preview[:55])
        for _, row in pool.iterrows():
            ans = re.sub(r"\s+", " ", str(row["provided_answer"]))
            if key[:35] in ans:
                return str(row["provided_answer"]), float(row["normalized_grade"])
        return None, None
    r = hits.iloc[0]
    return str(r["provided_answer"]), float(r["normalized_grade"])


def qwk(humans: list[float], preds: list[float], total: float) -> float:
    labels = np.round(np.arange(0, total + 0.125, 0.25), 4)
    # normalize pool alternative: use marks ladder
    label_to_i = {float(l): i for i, l in enumerate(labels)}
    n = len(labels)
    O = np.zeros((n, n), dtype=float)

    def snap(x: float) -> float:
        return float(labels[np.argmin(np.abs(labels - x))])

    for t, p in zip(humans, preds):
        O[label_to_i[snap(t)], label_to_i[snap(p)]] += 1
    W = np.array([[((i - j) / (n - 1)) ** 2 if n > 1 else 0.0 for j in range(n)] for i in range(n)])
    E = np.outer(O.sum(1), O.sum(0)) / max(O.sum(), 1)
    den = (W * E).sum()
    if den == 0:
        return 1.0 if (W * O).sum() == 0 else 0.0
    return float(1.0 - (W * O).sum() / den)


async def run_arm(
    qid: str,
    n: int,
    arm: str,
    skip_facets: bool,
    no_calibrate: bool,
    saf: pd.DataFrame | None,
    settings,
    llm: LLMClient,
    nli: NLIService | None,
) -> dict:
    pack = json.loads((CORRECTED / f"{qid}.json").read_text(encoding="utf-8"))
    smoke = json.loads((SMOKE / f"{qid}_grades.json").read_text(encoding="utf-8"))
    total = float(pack["total_marks"])
    pool = load_pool(qid, pack["question_text"], saf)

    students: list[StudentAnswer] = []
    gold_labels: list[dict] = []
    for s in smoke["students"][:n]:
        ans, norm = match_ans(pool, s["answer_preview"])
        if ans is None:
            print(f"  SKIP match {s['student_id']}")
            continue
        base = s["student_id"]
        students.append(StudentAnswer(student_id=base, answer_text=ans))
        human = round(float(norm) * total, 4)
        gold_labels.append(
            {
                "student_id": base,
                "human_normalized": norm,
                "human_score": human,
                "expected_score_range": [max(0.0, human - 0.01), human + 0.01],
                "expected_band": ("high" if norm >= 0.75 else "low" if norm <= 0.25 else "mid"),
            }
        )

    exam_id = f"cera_ab_{qid}_{arm}_n{len(students)}"
    exam_dir = EXAMS_ROOT / exam_id
    if exam_dir.exists():
        shutil.rmtree(exam_dir)

    # ExamInput.total_marks is int in model — use ceil/int as pack does
    tm = int(pack["total_marks"])
    exam = ExamInput(
        exam_id=exam_id,
        subject=f"CERA facets A/B — {qid} ({arm})",
        questions=[
            QuestionInput(
                question_id=qid,
                question_text=pack["question_text"],
                reference_answer=pack["reference_answer"],
                rubric=pack["rubric"],
                total_marks=tm,
                student_answers=students,
            )
        ],
    )
    cqas = [CQATuple.model_validate(c) for c in pack["cqa_tuples"]]

    pipe = GradingPipeline(
        llm,
        nli,
        settings=settings,
        exam_id=exam_id,
        exams_dir=str(EXAMS_ROOT),
        skip_facets=skip_facets,
    )
    # Lock CQAs before grade so CERA is skipped
    assert pipe.store is not None
    pipe.store.save_exam_config(exam)
    pipe.store.save_cqa_tuples(cqas)

    print(f"\n===== {qid} arm={arm} skip_facets={skip_facets} n={len(students)} =====")
    result = await pipe.run_grading_phase(
        exam,
        resume=True,  # pick up locked CQAs
        calibrate=not no_calibrate,
        calibrate_n=2,
        gold_labels=gold_labels,
    )

    # Finals: auto-aggregate when possible; for A/B, provisional-score deferred
    # concepts using CGR marks (no teacher in the loop).
    store = ExamStore(exam_id, exams_dir=str(EXAMS_ROOT), settings=settings)
    finals = store.load_final_results()
    if not finals:
        from scales.models.correction import CorrectionType, TeacherCorrection
        from scales.modules.aggregator import AggregatorModule

        # Synthetic corrections: accept CGR marks for deferred concepts (A/B only)
        corrections: list[TeacherCorrection] = []
        for cbte in result.cbte_results:
            if cbte.decision != TrustDecision.DEFER:
                continue
            cgr = next(
                (
                    r
                    for r in result.cgr_results
                    if r.student_id == cbte.student_id and r.concept_id == cbte.concept_id
                ),
                None,
            )
            if cgr is None:
                continue
            corrections.append(
                TeacherCorrection(
                    cbte_result_id=cbte.result_id,
                    student_id=cbte.student_id,
                    concept_id=cbte.concept_id,
                    system_verdict=cgr.verdict,
                    system_marks=cgr.marks_awarded,
                    teacher_verdict=cgr.verdict,
                    teacher_marks=cgr.marks_awarded,
                    teacher_comment="A/B provisional: CGR marks (deferred, no human review)",
                    correction_type=CorrectionType.AGREE,
                )
            )
        finals = AggregatorModule().compute_batch(
            question_id=qid,
            total_marks=tm,
            cqa_list=cqas,
            cgr_results=result.cgr_results,
            cbte_results=result.cbte_results,
            corrections=corrections,
            student_ids=list(result.graded_students),
        )
        store.save_final_results(finals)

    gold_by = {g["student_id"]: g for g in gold_labels}
    rows = []
    for fr in finals:
        g = gold_by[fr.student_id]
        human = float(g["human_score"])
        sys_m = float(fr.final_score)
        rows.append(
            {
                "student_id": fr.student_id,
                "human": human,
                "system": sys_m,
                "abs_err": abs(sys_m - human),
                "bias": sys_m - human,
                "trust": float(fr.overall_trust),
            }
        )

    defer_n = sum(1 for r in result.cbte_results if r.decision == TrustDecision.DEFER)
    accept_n = sum(1 for r in result.cbte_results if r.decision == TrustDecision.ACCEPT)
    humans = [r["human"] for r in rows]
    preds = [r["system"] for r in rows]
    mae = sum(r["abs_err"] for r in rows) / len(rows) if rows else None
    bias = sum(r["bias"] for r in rows) / len(rows) if rows else None
    over = sum(1 for r in rows if r["bias"] > 0.01)
    under = sum(1 for r in rows if r["bias"] < -0.01)
    exact = len(rows) - over - under

    out = {
        "question_id": qid,
        "arm": arm,
        "skip_facets": skip_facets,
        "exam_id": exam_id,
        "n_students": len(rows),
        "total_marks": tm,
        "mae": round(mae, 3) if mae is not None else None,
        "mean_bias": round(bias, 3) if bias is not None else None,
        "qwk": round(qwk(humans, preds, float(tm)), 3) if rows else None,
        "exact": exact,
        "over": over,
        "under": under,
        "deferred_concept_rows": defer_n,
        "accepted_concept_rows": accept_n,
        "deferred_count_status": result.deferred_count,
        "students": rows,
    }
    print(
        f"  MAE={out['mae']} bias={out['mean_bias']:+} QWK={out['qwk']} "
        f"over={over} under={under} exact={exact} defers={defer_n}"
    )
    return out


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--qids", nargs="+", default=DEFAULT_QIDS)
    ap.add_argument("--n", type=int, default=8)
    ap.add_argument("--no-nli", action="store_true")
    ap.add_argument("--no-calibrate", action="store_true")
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    EXAMS_ROOT.mkdir(parents=True, exist_ok=True)
    settings = get_settings()
    llm = LLMClient(settings.llm)
    nli = None
    if not args.no_nli:
        print("Loading NLI…")
        nli = NLIService(settings.nli.model_name, device=settings.nli.device)

    saf = None
    need = any(q not in LOCAL or not LOCAL[q].exists() for q in args.qids)
    if need:
        t = pq.read_table(
            CACHE,
            columns=["question", "provided_answer", "normalized_grade", "data_source"],
        )
        saf = t.to_pandas()
        saf = saf[saf["data_source"] == "SAF"]

    all_results = []
    for qid in args.qids:
        for arm, skip in (("facets", False), ("skip_facets", True)):
            res = await run_arm(
                qid,
                args.n,
                arm,
                skip,
                args.no_calibrate,
                saf,
                settings,
                llm,
                nli,
            )
            (OUT / f"{qid}_{arm}.json").write_text(
                json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8"
            )
            all_results.append(res)

    # Comparison table
    by_q: dict[str, dict] = {}
    for r in all_results:
        by_q.setdefault(r["question_id"], {})[r["arm"]] = r

    lines = [
        "# Full pipeline A/B — facets vs skip_facets",
        "",
        f"Run: {datetime.now(UTC).isoformat()}",
        "Pipeline: **locked CERA CQAs** → CGR → CBTE → Aggregator (no teacher review).",
        f"n={args.n} per question · no_nli={args.no_nli} · no_calibrate={args.no_calibrate}",
        "",
        "| Q | MAE facets | MAE skip | ΔMAE | QWK facets | QWK skip | bias facets | bias skip | defers F/S |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for qid in args.qids:
        f = by_q.get(qid, {}).get("facets")
        s = by_q.get(qid, {}).get("skip_facets")
        if not f or not s:
            continue
        dmae = (s["mae"] or 0) - (f["mae"] or 0)
        lines.append(
            f"| {qid} | {f['mae']} | {s['mae']} | {dmae:+.3f} | "
            f"{f['qwk']} | {s['qwk']} | {f['mean_bias']:+.3f} | {s['mean_bias']:+.3f} | "
            f"{f['deferred_concept_rows']}/{s['deferred_concept_rows']} |"
        )

    # Pooled
    def pool(arm: str):
        hs, ps, errs, biases = [], [], [], []
        for r in all_results:
            if r["arm"] != arm:
                continue
            for st in r["students"]:
                # normalize for pooled QWK
                tot = r["total_marks"]
                hs.append(st["human"] / tot)
                ps.append(st["system"] / tot)
                errs.append(st["abs_err"])
                biases.append(st["bias"])
        return hs, ps, errs, biases

    for arm in ("facets", "skip_facets"):
        hs, ps, errs, biases = pool(arm)
        if not errs:
            continue
        # pooled QWK on 0-1 ladder
        labels = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
        # reuse qwk with total=1
        pooled_qwk = qwk([h * 1 for h in hs], [p * 1 for p in ps], 1.0)
        # Fix: qwk snaps to 0.25 of total=1 — good
        lines += [
            "",
            f"## Pooled ({arm}, n={len(errs)})",
            f"- MAE (marks, unnormalized abs err mean): **{sum(errs) / len(errs):.3f}**",
            f"- Mean bias (sys−human marks): **{sum(biases) / len(biases):+.3f}**",
            f"- QWK (normalized 0–1): **{pooled_qwk:.3f}**",
        ]

    (OUT / "COMPARISON.md").write_text("\n".join(lines), encoding="utf-8")
    (OUT / "SUMMARY.json").write_text(
        json.dumps(
            {
                "run_ts": datetime.now(UTC).isoformat(),
                "qids": args.qids,
                "n": args.n,
                "no_nli": args.no_nli,
                "results": all_results,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print("\nWrote", OUT / "COMPARISON.md")


if __name__ == "__main__":
    asyncio.run(main())
