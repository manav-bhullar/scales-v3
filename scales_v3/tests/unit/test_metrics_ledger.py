"""Unit tests for metrics_ledger helpers."""

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
compute_post_review_metrics = _mod.compute_post_review_metrics


def test_compute_metrics_basic():
    grading = {
        "exam_id": "t",
        "cgr_results": [
            {
                "student_id": "S_HI",
                "concept_id": "Q1_C1",
                "verdict": "FULL",
                "marks_awarded": 1.0,
            },
            {
                "student_id": "S_HI",
                "concept_id": "Q1_C2",
                "verdict": "FULL",
                "marks_awarded": 1.0,
            },
            {
                "student_id": "S_LO",
                "concept_id": "Q1_C1",
                "verdict": "ABSENT",
                "marks_awarded": 0.0,
            },
            {
                "student_id": "S_LO",
                "concept_id": "Q1_C2",
                "verdict": "FULL",
                "marks_awarded": 1.0,
            },
        ],
        "cbte_results": [
            {"student_id": "S_HI", "concept_id": "Q1_C1", "decision": "ACCEPT"},
            {"student_id": "S_HI", "concept_id": "Q1_C2", "decision": "DEFER"},
            {"student_id": "S_LO", "concept_id": "Q1_C1", "decision": "ACCEPT"},
            {"student_id": "S_LO", "concept_id": "Q1_C2", "decision": "ACCEPT"},
        ],
    }
    gold = {
        "gold_labels": [
            {
                "student_id": "S_HI",
                "expected_band": "high",
                "expected_score_range": [1.0, 2.0],
            },
            {
                "student_id": "S_LO",
                "expected_band": "low",
                "expected_score_range": [0.0, 0.5],
            },
        ]
    }
    m = compute_metrics(grading, gold)
    assert m["n_items"] == 4
    assert m["defer_count"] == 1
    assert m["false_defer_count"] == 1  # S_HI C2 FULL+DEFER
    assert m["false_accept_count"] == 1  # S_LO C2 ACCEPT with marks>0
    # S_HI provisional = 1.0 (only ACCEPT), in [1,2]; S_LO = 1.0 out of [0,0.5]
    assert m["band_hit_rate"] == 0.5


def test_compute_post_review_metrics_uses_final_scores():
    grading = {
        "exam_id": "t",
        "cbte_results": [
            {"student_id": "S_HI", "concept_id": "Q1_C1", "decision": "ACCEPT"},
            {"student_id": "S_HI", "concept_id": "Q1_C2", "decision": "DEFER"},
            {"student_id": "S_LO", "concept_id": "Q1_C1", "decision": "ACCEPT"},
            {"student_id": "S_LO", "concept_id": "Q1_C2", "decision": "ACCEPT"},
        ],
    }
    # After review, S_HI's deferred concept is agreed -> final 2.0 (now in band)
    finals = {
        "final_results": [
            {"student_id": "S_HI", "final_score": 2.0},
            {"student_id": "S_LO", "final_score": 1.0},
        ]
    }
    corrections = {
        "corrections": [
            {"correction_type": "AGREE"},
        ]
    }
    gold = {
        "gold_labels": [
            {
                "student_id": "S_HI",
                "expected_band": "high",
                "expected_score_range": [1.0, 2.0],
            },
            {
                "student_id": "S_LO",
                "expected_band": "low",
                "expected_score_range": [0.0, 0.5],
            },
        ]
    }
    m = compute_post_review_metrics(grading, finals, corrections, gold)
    assert m["defer_count"] == 1
    assert m["review_resolved"] == 1
    assert m["correction_types"] == {"AGREE": 1}
    # S_HI final 2.0 in [1,2] -> hit; S_LO 1.0 out of [0,0.5] -> miss
    assert m["band_hit_rate"] == 0.5
    assert m["n_students"] == 2
