#!/usr/bin/env python3
"""Pre-grade calibration smoke: extract CQAs (or load), grade a few gold answers,
flag concepts that ABSENT high-band students.

Usage (from scales_v3/):
  .venv/bin/python scripts/calibrate_cqas.py \\
    --exam-json data/e2e_eval/wave5_real/saf_wave6_picked/frame_bursting_n10/exam.json \\
    --gold-json data/e2e_eval/wave5_real/saf_wave6_picked/frame_bursting_n10/gold_labels.json \\
    --n 3
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from collections import defaultdict
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
if str(PROJECT) not in sys.path:
    sys.path.insert(0, str(PROJECT))


async def main() -> int:
    parser = argparse.ArgumentParser(description="CQA calibration smoke before batch grade")
    parser.add_argument("--exam-json", required=True)
    parser.add_argument("--gold-json", required=True)
    parser.add_argument("--n", type=int, default=3, help="Number of gold answers to grade")
    parser.add_argument(
        "--cqa-json",
        default="",
        help="Optional existing cqa_tuples.json (skip CERA if provided)",
    )
    parser.add_argument(
        "--prefer-bands",
        default="high,mid_high,mid",
        help="Comma-separated preferred gold bands to sample first",
    )
    args = parser.parse_args()

    from scales.config import get_settings
    from scales.models.cqa import CQATuple
    from scales.models.exam import ExamInput
    from scales.modules.cera import CERAModule
    from scales.modules.cgr import CGRModule
    from scales.services.llm_client import LLMClient

    exam_path = Path(args.exam_json)
    if not exam_path.is_absolute():
        exam_path = PROJECT / exam_path
    gold_path = Path(args.gold_json)
    if not gold_path.is_absolute():
        gold_path = PROJECT / gold_path

    raw = json.loads(exam_path.read_text(encoding="utf-8"))
    exam = ExamInput.model_validate(raw["exam"] if "exam" in raw else raw)
    question = exam.questions[0]
    gold_doc = json.loads(gold_path.read_text(encoding="utf-8"))
    gold_rows = gold_doc.get("gold_labels", gold_doc)
    by_sid = {g["student_id"]: g for g in gold_rows}
    answers = {a.student_id: a.answer_text for a in question.student_answers}

    prefer = [b.strip() for b in args.prefer_bands.split(",") if b.strip()]
    ordered: list[str] = []
    for band in prefer:
        for sid, g in by_sid.items():
            if g.get("expected_band") == band and sid in answers and sid not in ordered:
                ordered.append(sid)
    for sid in answers:
        if sid not in ordered:
            ordered.append(sid)
    sample = ordered[: max(1, args.n)]

    settings = get_settings()
    llm = LLMClient(settings.llm)

    if args.cqa_json:
        cqa_path = Path(args.cqa_json)
        if not cqa_path.is_absolute():
            cqa_path = PROJECT / cqa_path
        payload = json.loads(cqa_path.read_text(encoding="utf-8"))
        cqa_list = [CQATuple.model_validate(c) for c in payload.get("cqa_tuples", payload)]
        print(f"Loaded {len(cqa_list)} CQAs from {cqa_path}")
    else:
        cera = CERAModule(llm, settings)
        out = await cera.extract_concepts(question)
        cqa_list = out.cqa_tuples
        out_path = exam_path.parent / "cqa_calibration.json"
        out_path.write_text(
            json.dumps(
                {
                    "exam_id": exam.exam_id,
                    "cqa_tuples": [c.model_dump(mode="json") for c in cqa_list],
                    "extraction_metadata": out.extraction_metadata,
                },
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        print(f"CERA wrote {out_path} ({len(cqa_list)} concepts)")

    print("\nConcepts:")
    for c in cqa_list:
        print(
            f"  {c.concept_id} [{c.evidence_mode}] marks={c.marks} "
            f"facets={c.evidence_facets} partial={c.partial_credit_rule!r}"
        )

    cgr = CGRModule(llm, settings)
    absent: dict[str, list[str]] = defaultdict(list)
    results: list[dict] = []

    for sid in sample:
        band = by_sid.get(sid, {}).get("expected_band", "?")
        human = by_sid.get(sid, {}).get("human_score_3") or by_sid.get(sid, {}).get(
            "expected_score_range", ["?", "?"]
        )
        print(f"\n--- {sid} band={band} human={human} ---")
        for cqa in cqa_list:
            gr = await cgr.grade_concept(
                student_id=sid,
                student_answer=answers[sid],
                cqa=cqa,
                question_text=question.question_text,
            )
            print(f"  {cqa.concept_id}: {gr.verdict.value}/{gr.marks_awarded}")
            results.append(
                {
                    "student_id": sid,
                    "concept_id": cqa.concept_id,
                    "verdict": gr.verdict.value,
                    "marks_awarded": gr.marks_awarded,
                    "band": band,
                }
            )
            if gr.verdict.value == "ABSENT" and band in ("high", "mid_high"):
                absent[cqa.concept_id].append(sid)

    print("\n=== Calibration flags ===")
    if not absent:
        print("OK: no ABSENT on high/mid_high sample answers")
    else:
        for cid, sids in absent.items():
            print(
                f"FLAG {cid}: ABSENT on high-band sample {sids} — "
                "review evidence_mode / facets / target_criteria before batch grade"
            )

    report = exam_path.parent / "calibration_report.json"
    report.write_text(
        json.dumps(
            {
                "sample_students": sample,
                "results": results,
                "flags": {k: v for k, v in absent.items()},
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"\nWrote {report}")
    return 1 if absent else 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
