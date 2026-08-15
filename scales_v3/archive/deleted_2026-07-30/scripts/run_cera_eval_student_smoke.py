#!/usr/bin/env python3
"""Grade 10 random SAF students per corrected CERA-eval question."""

from __future__ import annotations

import asyncio
import json
import random
from datetime import UTC, datetime
from pathlib import Path

import pyarrow.parquet as pq

from scales.config import get_settings
from scales.models.cqa import CQATuple
from scales.modules.cgr import CGRModule
from scales.services.llm_client import LLMClient

PROJECT = Path(__file__).resolve().parents[1]
CORRECTED = PROJECT / "data/cera_eval/runs/cera_eval_v1_corrected"
OUT = PROJECT / "data/cera_eval/runs/student_smoke_n10"
CACHE = (
    Path.home()
    / ".cache/huggingface/hub/datasets--Meyerger--ASAG2024"
    / "snapshots/9a7a179de4e227f5e78625bc9ded2d8761f1ff09/train.parquet"
)
N_STUDENTS = 10
SEED = 42


async def grade_question(cgr: CGRModule, qid: str, payload: dict, answers: list[dict]) -> dict:
    cqas = [CQATuple.model_validate(c) for c in payload["cqa_tuples"]]
    qtext = payload["question_text"]
    total = float(payload["total_marks"])
    rows = []
    for ans in answers:
        sid = ans["student_id"]
        text = ans["answer_text"]
        concept_rows = []
        awarded = 0.0
        for cqa in cqas:
            result = await cgr.grade_concept(
                student_id=sid,
                student_answer=text,
                cqa=cqa,
                question_text=qtext,
            )
            marks = float(result.marks_awarded)
            awarded += marks
            concept_rows.append(
                {
                    "concept_id": cqa.concept_id,
                    "role": cqa.evidence_role,
                    "min_count": cqa.min_count,
                    "max_marks": cqa.marks,
                    "verdict": result.verdict.value
                    if hasattr(result.verdict, "value")
                    else str(result.verdict),
                    "marks_awarded": marks,
                    "evidence_span": result.evidence_span,
                }
            )
        rows.append(
            {
                "student_id": sid,
                "human_norm": ans["human_norm"],
                "human_est_marks": round(ans["human_norm"] * total, 2),
                "system_marks": round(awarded, 2),
                "abs_err": round(abs(awarded - ans["human_norm"] * total), 2),
                "answer_preview": text[:180].replace("\n", " "),
                "concepts": concept_rows,
            }
        )
        print(f"  {qid} {sid}: sys={awarded:.2f}/{total} human≈{ans['human_norm'] * total:.2f}")
    mae = sum(r["abs_err"] for r in rows) / max(1, len(rows))
    return {
        "question_id": qid,
        "total_marks": total,
        "n_students": len(rows),
        "mae": round(mae, 3),
        "students": rows,
    }


async def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    settings = get_settings()
    client = LLMClient(settings.llm)
    cgr = CGRModule(client, settings)

    df = pq.read_table(CACHE).to_pandas()
    saf = df[df["data_source"] == "SAF"]
    rng = random.Random(SEED)

    summary = []
    for path in sorted(CORRECTED.glob("CE*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        qid = payload["id"]
        qtext = payload["question_text"]
        # Match SAF rows by question prefix (dataset questions can be longer)
        subset = saf[saf["question"].str.startswith(qtext[:80])]
        if subset.empty:
            # fallback: containment either way
            subset = saf[saf["question"].apply(lambda q: qtext[:60] in q or q[:60] in qtext)]
        if subset.empty:
            print(f"ERR {qid}: no SAF rows found")
            summary.append({"question_id": qid, "status": "no_students"})
            continue
        pool = subset.to_dict("records")
        picked = rng.sample(pool, k=min(N_STUDENTS, len(pool)))
        answers = [
            {
                "student_id": f"{qid}_S{i:02d}",
                "answer_text": r["provided_answer"] or "",
                "human_norm": float(r["normalized_grade"]),
            }
            for i, r in enumerate(picked, 1)
        ]
        print(f"\n=== {qid} n={len(answers)} ===")
        report = await grade_question(cgr, qid, payload, answers)
        (OUT / f"{qid}_grades.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        summary.append(
            {
                "question_id": qid,
                "status": "ok",
                "mae": report["mae"],
                "total_marks": report["total_marks"],
                "n_students": report["n_students"],
            }
        )

    out = {
        "run_ts": datetime.now(UTC).isoformat(),
        "n_students_per_q": N_STUDENTS,
        "seed": SEED,
        "summary": summary,
        "overall_mae": round(
            sum(s["mae"] for s in summary if s.get("status") == "ok")
            / max(1, sum(1 for s in summary if s.get("status") == "ok")),
            3,
        ),
    }
    (OUT / "SUMMARY.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("\nSUMMARY")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
