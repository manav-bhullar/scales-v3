#!/usr/bin/env python3
"""Ablation: grade corrected CQAs with CGRModule(skip_facets=True).

Reuses student_smoke_n10 answers (first N per question). Compares MAE vs facet-based
smoke marks. Writes under data/cera_eval/runs/nofacets_ablation_n8/.

Default questions: remaining eval set excl CE02/CE09 (gold issues) and optionally
CE04 (already in ce04_nofacets_n8 with rewritten criteria).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq

from scales.config import get_settings
from scales.models.cqa import CQATuple
from scales.modules.cgr import CGRModule
from scales.services.llm_client import LLMClient

PROJECT = Path(__file__).resolve().parents[1]
CORRECTED = PROJECT / "data/cera_eval/runs/cera_eval_v1_corrected"
SMOKE = PROJECT / "data/cera_eval/runs/student_smoke_n10"
OUT = PROJECT / "data/cera_eval/runs/nofacets_ablation_n8"
CACHE = (
    Path.home()
    / ".cache/huggingface/hub/datasets--Meyerger--ASAG2024"
    / "snapshots/9a7a179de4e227f5e78625bc9ded2d8761f1ff09/train.parquet"
)
LOCAL_PARQUET = {
    "CE01": PROJECT
    / "data/e2e_eval/wave5_real/saf_wave6_picked/wave6_coarse_n20/dll_service_classes/source.parquet",
    "CE04": PROJECT
    / "data/e2e_eval/wave5_real/saf_wave6_picked/wave6_coarse_n20/frame_bursting/source.parquet",
}

DEFAULT_QIDS = ["CE01", "CE03", "CE05", "CE06", "CE07", "CE08", "CE10"]


def load_pool(qid: str, qtext: str, saf: pd.DataFrame | None) -> tuple[pd.DataFrame, pd.DataFrame]:
    if qid in LOCAL_PARQUET and LOCAL_PARQUET[qid].exists():
        return pd.read_parquet(LOCAL_PARQUET[qid]), saf  # type: ignore[return-value]
    assert saf is not None
    key = re.sub(r"\s+", " ", qtext)
    for n in (50, 35, 25):
        m = saf[saf["question"].astype(str).str.contains(re.escape(key[:n]), case=False, na=False)]
        if len(m) >= 5:
            return m, saf
    words = re.findall(r"[A-Za-z]{4,}", qtext)[:6]
    m = saf[
        saf["question"]
        .astype(str)
        .str.contains(".*".join(words[:4]), case=False, na=False, regex=True)
    ]
    return m, saf


def match_ans(pool: pd.DataFrame, preview: str, total: float):
    hits = pool[pool["provided_answer"].astype(str).str.startswith(preview[:50].rstrip(), na=False)]
    if len(hits) == 0:
        key = re.sub(r"\s+", " ", preview[:55])
        for _, row in pool.iterrows():
            ans = re.sub(r"\s+", " ", str(row["provided_answer"]))
            if key[:35] in ans:
                return (
                    str(row["provided_answer"]),
                    float(row["normalized_grade"]) * total,
                    float(row["normalized_grade"]),
                )
        return None, None, None
    r = hits.iloc[0]
    return (
        str(r["provided_answer"]),
        float(r["normalized_grade"]) * total,
        float(r["normalized_grade"]),
    )


async def grade_question(
    qid: str,
    n: int,
    cgr: CGRModule,
    saf: pd.DataFrame | None,
) -> dict:
    pack = json.loads((CORRECTED / f"{qid}.json").read_text(encoding="utf-8"))
    smoke = json.loads((SMOKE / f"{qid}_grades.json").read_text(encoding="utf-8"))
    total = float(pack["total_marks"])
    cqas = [CQATuple.model_validate(c) for c in pack["cqa_tuples"]]
    pool, _ = load_pool(qid, pack["question_text"], saf)

    rows = []
    for s in smoke["students"][:n]:
        ans, human, norm = match_ans(pool, s["answer_preview"], total)
        if ans is None:
            print(f"  SKIP {s['student_id']} (no SAF match)")
            continue
        sid = s["student_id"]
        print(f"  {sid} human={human}")
        results = await cgr.grade_all_concepts(
            student_id=sid,
            student_answer=ans,
            cqa_list=cqas,
            question_text=pack["question_text"],
        )
        concepts = []
        sys_marks = 0.0
        for r, cqa in zip(results, cqas):
            concepts.append(
                {
                    "concept_id": r.concept_id,
                    "role_in_cqa": cqa.evidence_role,
                    "max_marks": cqa.marks,
                    "verdict": r.verdict.value,
                    "marks_awarded": r.marks_awarded,
                    "evidence_span": r.evidence_span,
                    "reasoning": r.reasoning,
                }
            )
            sys_marks += r.marks_awarded
            print(
                f"    {r.concept_id}: {r.verdict.value} {r.marks_awarded:g} "
                f"{(r.evidence_span or '')[:60]!r}"
            )
        facet_sys = float(s["system_marks"])
        rows.append(
            {
                "student_id": sid,
                "human_norm": norm,
                "human_est_marks": human,
                "system_marks_nofacets": sys_marks,
                "system_marks_with_facets": facet_sys,
                "abs_err_nofacets": abs(sys_marks - human),
                "abs_err_with_facets": abs(facet_sys - human),
                "answer": ans,
                "concepts": concepts,
            }
        )

    mae_nf = sum(r["abs_err_nofacets"] for r in rows) / len(rows) if rows else None
    mae_f = sum(r["abs_err_with_facets"] for r in rows) / len(rows) if rows else None
    return {
        "question_id": qid,
        "mode": "skip_facets=True (CGR prompt omits facets/keywords/variants)",
        "n_students": len(rows),
        "total_marks": total,
        "mae_nofacets": round(mae_nf, 3) if mae_nf is not None else None,
        "mae_with_facets_same_students": round(mae_f, 3) if mae_f is not None else None,
        "students": rows,
    }


def write_analysis(out_dir: Path, results: list[dict]) -> None:
    lines = [
        "# No-facets ablation (CGR skip_facets=True)",
        "",
        "CGR prompt receives empty Evidence Facets / keywords / variants; role forced to",
        "`synonym_set` in the prompt. Target Criteria from corrected CQAs unchanged.",
        "",
        "| Question | n | MAE no-facets | MAE with-facets (same students) | Δ MAE |",
        "|---|---:|---:|---:|---:|",
    ]
    for q in results:
        nf = q["mae_nofacets"]
        f = q["mae_with_facets_same_students"]
        delta = (nf - f) if nf is not None and f is not None else None
        d_s = f"{delta:+.3f}" if delta is not None else "—"
        lines.append(f"| {q['question_id']} | {q['n_students']} | {nf} | {f} | {d_s} |")
    lines += ["", "(negative Δ = no-facets closer to human)", ""]

    for q in results:
        total = q["total_marks"]
        lines += [
            "=" * 72,
            "",
            f"## {q['question_id']} · MAE no-facets {q['mae_nofacets']} · "
            f"with-facets {q['mae_with_facets_same_students']}",
            "",
        ]
        for r in q["students"]:
            lines += [
                "-" * 72,
                f"### {r['student_id']}",
                "",
                "**Marks**",
                "",
                "| Source | Value |",
                "|---|---|",
                f"| **Human evaluator** | **{r['human_est_marks']:g} / {total:g}** |",
                f"| System (no facets) | **{r['system_marks_nofacets']:g} / {total:g}** |",
                f"| System (with facets) | {r['system_marks_with_facets']:g} / {total:g} |",
                f"| abs err no-facets | {r['abs_err_nofacets']:g} |",
                "",
                "**Student answer**",
                "",
                "```",
                r["answer"].strip(),
                "```",
                "",
                "**Our check (skip_facets)**",
                "",
                "| Concept | Verdict | Marks | Evidence |",
                "|---|---|---:|---|",
            ]
            for c in r["concepts"]:
                evid = (c["evidence_span"] or "—").replace("|", "\\|").replace("\n", " ")
                if len(evid) > 280:
                    evid = evid[:277] + "…"
                lines.append(
                    f"| `{c['concept_id']}` | {c['verdict']} | "
                    f"{c['marks_awarded']:g}/{c['max_marks']:g} | {evid} |"
                )
            lines.append("")

    (out_dir / "ANALYSIS.md").write_text("\n".join(lines), encoding="utf-8")


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=8)
    ap.add_argument("--qids", nargs="+", default=DEFAULT_QIDS)
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    settings = get_settings()
    cgr = CGRModule(LLMClient(settings.llm), settings, skip_facets=True)

    saf = None
    need_saf = any(q not in LOCAL_PARQUET or not LOCAL_PARQUET[q].exists() for q in args.qids)
    if need_saf:
        t = pq.read_table(
            CACHE,
            columns=["question", "provided_answer", "grade", "normalized_grade", "data_source"],
        )
        saf = t.to_pandas()
        saf = saf[saf["data_source"] == "SAF"]

    results = []
    for qid in args.qids:
        print(f"\n===== {qid} skip_facets n={args.n} =====")
        qres = await grade_question(qid, args.n, cgr, saf)
        (OUT / f"{qid}_grades.json").write_text(
            json.dumps(qres, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        results.append(qres)
        print(
            f"  MAE no-facets={qres['mae_nofacets']}  "
            f"with-facets={qres['mae_with_facets_same_students']}"
        )

    summary = {
        "run_ts": datetime.now(UTC).isoformat(),
        "n_per_question": args.n,
        "skip_facets": True,
        "qids": args.qids,
        "note": (
            "CGRModule(skip_facets=True) blanks facets/keywords/variants in prompt; "
            "forces synonym_set in prompt. CQAs themselves unchanged on disk."
        ),
        "per_question": [
            {
                "question_id": q["question_id"],
                "n": q["n_students"],
                "mae_nofacets": q["mae_nofacets"],
                "mae_with_facets": q["mae_with_facets_same_students"],
            }
            for q in results
        ],
    }
    (OUT / "SUMMARY.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    write_analysis(OUT, results)
    print("\nWrote", OUT)


if __name__ == "__main__":
    asyncio.run(main())
