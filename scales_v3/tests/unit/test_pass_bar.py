"""L4 — Silent-zero metric + executable Wave4 pass bar."""

from __future__ import annotations

import importlib.util
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_SPEC = importlib.util.spec_from_file_location(
    "metrics_ledger",
    _ROOT / "scripts" / "metrics_ledger.py",
)
assert _SPEC and _SPEC.loader
_mod = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_mod)
compute_metrics = _mod.compute_metrics
evaluate_pass_bar = _mod.evaluate_pass_bar
format_pass_bar = _mod.format_pass_bar


def _grading_silent_zero_case() -> tuple[dict, dict]:
    """GOOD student: PARTIAL emptied to ABSENT, Tier-1 ACCEPT — invisible to false_accept."""
    grading = {
        "exam_id": "t",
        "cgr_results": [
            {
                "student_id": "S_GOOD",
                "concept_id": "Q1_C1",
                "verdict": "ABSENT",
                "marks_awarded": 0.0,
            },
            {
                "student_id": "S_GOOD",
                "concept_id": "Q1_C2",
                "verdict": "FULL",
                "marks_awarded": 1.0,
            },
            {
                "student_id": "S_LOW",
                "concept_id": "Q1_C1",
                "verdict": "ABSENT",
                "marks_awarded": 0.0,
            },
            {
                "student_id": "S_LOW",
                "concept_id": "Q1_C2",
                "verdict": "ABSENT",
                "marks_awarded": 0.0,
            },
        ],
        "cbte_results": [
            {"student_id": "S_GOOD", "concept_id": "Q1_C1", "decision": "ACCEPT"},
            {"student_id": "S_GOOD", "concept_id": "Q1_C2", "decision": "ACCEPT"},
            {"student_id": "S_LOW", "concept_id": "Q1_C1", "decision": "ACCEPT"},
            {"student_id": "S_LOW", "concept_id": "Q1_C2", "decision": "ACCEPT"},
        ],
    }
    gold = {
        "gold_labels": [
            {
                "student_id": "S_GOOD",
                "expected_band": "high",
                "expected_score_range": [1.5, 2.0],
            },
            {
                "student_id": "S_LOW",
                "expected_band": "low",
                "expected_score_range": [0.0, 0.0],
            },
        ]
    }
    return grading, gold


def test_silent_zero_counts_accepted_zeros_on_non_low():
    grading, gold = _grading_silent_zero_case()
    m = compute_metrics(grading, gold)
    assert m["false_accept_count"] == 0  # low students got 0 — safety OK
    assert m["silent_zero_count"] == 1  # S_GOOD C1
    assert m["silent_zero_by_verdict"] == {"ABSENT": 1}
    assert m["zeroed_students"] == []  # S_GOOD still has 1.0 provisional
    assert m["underscored_students"] == 1  # S_GOOD 1.0 < 1.5


def test_pass_bar_fails_on_silent_zero_and_high_miss():
    grading, gold = _grading_silent_zero_case()
    m = compute_metrics(grading, gold)
    # This fixture stands in for concept-level human gold confirming that the
    # accepted zero was unexpected.
    m["silent_zero_gold_aware"] = True
    report = evaluate_pass_bar(m)
    assert report["pass"] is False
    assert "no_silent_zeros" in report["failed"]
    assert "high_band_students_in_band" in report["failed"]
    assert "no_false_accept_on_low" not in report["failed"]
    text = format_pass_bar(report)
    assert "PASS BAR: FAIL" in text
    assert "no_silent_zeros" in text


def test_silent_zero_candidate_does_not_gate_without_concept_gold():
    grading, gold = _grading_silent_zero_case()
    m = compute_metrics(grading, gold)
    assert m["silent_zero_count"] == 1
    assert m["silent_zero_gold_aware"] is False
    report = evaluate_pass_bar(m)
    criterion = next(c for c in report["criteria"] if c["name"] == "no_silent_zeros")
    assert criterion["applicable"] is False
    assert "no_silent_zeros" not in report["failed"]


def test_pass_bar_passes_clean_smoke():
    grading = {
        "exam_id": "t",
        "cgr_results": [
            {"student_id": "G", "concept_id": "Q1_C1", "verdict": "FULL", "marks_awarded": 1.0},
            {"student_id": "G", "concept_id": "Q1_C2", "verdict": "FULL", "marks_awarded": 1.0},
            {"student_id": "M", "concept_id": "Q1_C1", "verdict": "PARTIAL", "marks_awarded": 0.5},
            {"student_id": "M", "concept_id": "Q1_C2", "verdict": "ABSENT", "marks_awarded": 0.0},
            {"student_id": "L", "concept_id": "Q1_C1", "verdict": "ABSENT", "marks_awarded": 0.0},
            {"student_id": "L", "concept_id": "Q1_C2", "verdict": "ABSENT", "marks_awarded": 0.0},
        ],
        "cbte_results": [
            {"student_id": "G", "concept_id": "Q1_C1", "decision": "ACCEPT"},
            {"student_id": "G", "concept_id": "Q1_C2", "decision": "ACCEPT"},
            {"student_id": "M", "concept_id": "Q1_C1", "decision": "ACCEPT"},
            {"student_id": "M", "concept_id": "Q1_C2", "decision": "ACCEPT"},
            {"student_id": "L", "concept_id": "Q1_C1", "decision": "ACCEPT"},
            {"student_id": "L", "concept_id": "Q1_C2", "decision": "ACCEPT"},
        ],
    }
    gold = {
        "gold_labels": [
            {"student_id": "G", "expected_band": "high", "expected_score_range": [1.5, 2.0]},
            {"student_id": "M", "expected_band": "mid_low", "expected_score_range": [0.5, 1.5]},
            {"student_id": "L", "expected_band": "low", "expected_score_range": [0.0, 0.5]},
        ]
    }
    m = compute_metrics(grading, gold)
    report = evaluate_pass_bar(m)
    assert report["pass"] is True
    assert report["failed"] == []


def test_pass_bar_flags_defer_rate_and_all_mid_zero():
    grading = {
        "exam_id": "t",
        "cgr_results": [
            {"student_id": "G", "concept_id": "Q1_C1", "verdict": "FULL", "marks_awarded": 1.0},
            {"student_id": "M", "concept_id": "Q1_C1", "verdict": "ABSENT", "marks_awarded": 0.0},
            {"student_id": "L", "concept_id": "Q1_C1", "verdict": "ABSENT", "marks_awarded": 0.0},
        ],
        "cbte_results": [
            {"student_id": "G", "concept_id": "Q1_C1", "decision": "DEFER"},
            {"student_id": "M", "concept_id": "Q1_C1", "decision": "ACCEPT"},
            {"student_id": "L", "concept_id": "Q1_C1", "decision": "ACCEPT"},
        ],
    }
    gold = {
        "gold_labels": [
            {"student_id": "G", "expected_band": "high", "expected_score_range": [0.5, 1.0]},
            {"student_id": "M", "expected_band": "mid", "expected_score_range": [0.5, 1.0]},
            {"student_id": "L", "expected_band": "low", "expected_score_range": [0.0, 0.0]},
        ]
    }
    m = compute_metrics(grading, gold)
    # defer 1/3 ≈ 0.333 — under 0.40; but force fail with low limit
    report = evaluate_pass_bar(m, max_defer_rate=0.20)
    assert "defer_rate_within_limit" in report["failed"]
    assert "mid_band_not_all_zero" in report["failed"]
    assert "high_band_students_in_band" in report["failed"]  # G provisional 0
