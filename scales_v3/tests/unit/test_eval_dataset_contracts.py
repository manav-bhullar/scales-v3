"""L1 — Eval dataset contracts (roadmap Phase B / Wave4 Step 0).

These fail fast if exam.json and gold_labels.json drift apart, so metrics_ledger
cannot silently skip students and inflate band-hit.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from scales.models.exam import ExamInput

PROJECT = Path(__file__).resolve().parents[2]
EVAL_DIR = PROJECT / "data" / "e2e_eval"
ALLOWED_BANDS = {"high", "mid", "mid_low", "low"}


def _discover_exam_pairs() -> list[tuple[str, Path, Path]]:
    pairs: list[tuple[str, Path, Path]] = []
    for exam_path in sorted(EVAL_DIR.rglob("exam.json")):
        gold_path = exam_path.parent / "gold_labels.json"
        if not gold_path.exists():
            continue
        rel = exam_path.parent.relative_to(EVAL_DIR).as_posix()
        pairs.append((rel, exam_path, gold_path))
    return pairs


EXAM_PAIRS = _discover_exam_pairs()


@pytest.mark.contracts
def test_eval_exam_pairs_discovered():
    assert EXAM_PAIRS, f"No exam.json+gold_labels.json pairs under {EVAL_DIR}"
    keys = {k for k, *_ in EXAM_PAIRS}
    assert "wave3" in keys or any(k.startswith("wave3") for k in keys)
    assert any("wave4" in k for k in keys)


@pytest.mark.contracts
@pytest.mark.parametrize("key,exam_path,gold_path", EXAM_PAIRS, ids=[k for k, *_ in EXAM_PAIRS])
def test_exam_gold_student_ids_match(key: str, exam_path: Path, gold_path: Path):
    payload = json.loads(exam_path.read_text(encoding="utf-8"))
    exam = ExamInput.model_validate(payload.get("exam", payload))
    gold = json.loads(gold_path.read_text(encoding="utf-8"))

    assert exam.exam_id, f"{key}: exam_id empty"
    assert gold.get("exam_id") == exam.exam_id, (
        f"{key}: gold exam_id {gold.get('exam_id')!r} != exam {exam.exam_id!r}"
    )

    assert len(exam.questions) == 1, f"{key}: smoke exams should be single-question"
    question = exam.questions[0]
    assert gold.get("question_id") == question.question_id
    assert gold.get("total_marks") == question.total_marks
    assert question.total_marks > 0
    assert question.reference_answer.strip()
    assert question.rubric.strip()

    exam_ids = [a.student_id for a in question.student_answers]
    gold_rows = gold["gold_labels"]
    gold_ids = [g["student_id"] for g in gold_rows]

    assert len(exam_ids) == len(set(exam_ids)), f"{key}: duplicate student_id in exam"
    assert len(gold_ids) == len(set(gold_ids)), f"{key}: duplicate student_id in gold"
    assert set(exam_ids) == set(gold_ids), (
        f"{key}: exam/gold student mismatch "
        f"only_in_exam={set(exam_ids) - set(gold_ids)} "
        f"only_in_gold={set(gold_ids) - set(exam_ids)}"
    )

    for row in gold_rows:
        band = row.get("expected_band")
        assert band in ALLOWED_BANDS, f"{key}/{row['student_id']}: bad band {band!r}"
        lo, hi = row["expected_score_range"]
        assert 0 <= lo <= hi <= question.total_marks, (
            f"{key}/{row['student_id']}: range [{lo},{hi}] vs total {question.total_marks}"
        )
        if band == "low":
            assert hi <= 0.5, f"{key}/{row['student_id']}: low band hi must be ≤ 0.5"


@pytest.mark.contracts
def test_wave4_smoke_shape():
    """Wave4 smoke exams: 8 answers, 2 per band family."""
    wave4 = EVAL_DIR / "wave4"
    folders = [
        wave4 / "os1_process_vs_thread",
        wave4 / "cn2_gbn_vs_sr",
        wave4 / "db1_acid",
    ]
    for folder in folders:
        exam = ExamInput.model_validate(
            json.loads((folder / "exam.json").read_text(encoding="utf-8"))["exam"]
        )
        gold = json.loads((folder / "gold_labels.json").read_text(encoding="utf-8"))
        answers = exam.questions[0].student_answers
        assert len(answers) == 8, f"{folder.name}: expected 8 smoke answers"
        bands = [g["expected_band"] for g in gold["gold_labels"]]
        assert bands.count("high") == 2
        assert bands.count("low") == 2
        assert sum(1 for b in bands if b in ("mid", "mid_low")) == 4
