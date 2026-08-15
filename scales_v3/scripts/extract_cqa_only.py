"""Run CERA only (no CGR/CBTE) for human concept review before grading.

Usage (from scales_v3/):
  .venv/Scripts/python.exe scripts/extract_cqa_only.py \
    --exam-json data/e2e_eval/wave5_real/mohler_bst_delete/exam.json
"""

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

from scales.config import get_settings
from scales.models.exam import ExamInput
from scales.modules.cera import CERAModule
from scales.services.llm_client import LLMClient

PROJECT = Path(__file__).resolve().parents[1]


async def main() -> None:
    parser = argparse.ArgumentParser(description="CERA-only concept extraction")
    parser.add_argument("--exam-json", required=True)
    parser.add_argument(
        "--out",
        default="",
        help="Output path for cqa_tuples.json (default: beside exam.json)",
    )
    args = parser.parse_args()

    exam_path = Path(args.exam_json)
    if not exam_path.is_absolute():
        exam_path = PROJECT / exam_path
    raw = json.loads(exam_path.read_text(encoding="utf-8"))
    exam = ExamInput.model_validate(raw["exam"] if "exam" in raw else raw)
    question = exam.questions[0]

    settings = get_settings()
    client = LLMClient(settings.llm)
    cera = CERAModule(client, settings)
    out = await cera.extract_concepts(question)

    payload = {
        "exam_id": exam.exam_id,
        "question_id": question.question_id,
        "question_text": question.question_text,
        "reference_answer": question.reference_answer,
        "total_marks": question.total_marks,
        "marks_sum": sum(c.marks for c in out.cqa_tuples),
        "cqa_tuples": [c.model_dump(mode="json") for c in out.cqa_tuples],
        "extraction_metadata": out.extraction_metadata,
        "status": "awaiting_human_cera_review",
    }

    out_path = Path(args.out) if args.out else exam_path.parent / "cqa_review.json"
    if not out_path.is_absolute():
        out_path = PROJECT / out_path
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {out_path}")
    print(
        f"Concepts: {len(out.cqa_tuples)} | marks sum={payload['marks_sum']} / {question.total_marks}"
    )
    for c in out.cqa_tuples:
        print(f"  {c.concept_id} ({c.marks}): {c.knowledge_point}")


if __name__ == "__main__":
    asyncio.run(main())
