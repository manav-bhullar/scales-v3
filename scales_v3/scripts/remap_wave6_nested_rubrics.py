#!/usr/bin/env python3
"""Remap Wave6 nested CQAs under coarser teacher rubric buckets.

Keeps existing concept text / marks / grading results. Only updates:
  - question.rubric + rubric_items
  - each CQA's rubric_item_id
  - teacher_calibration.json (reset to match new buckets)

Does NOT re-run CERA or CGR.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
PACK = PROJECT / "data/e2e_eval/wave5_real/saf_wave6_picked/wave6_coarse_n20"

# concept_id → new rubric_item_id
REMAP: dict[str, dict] = {
    "e2e_wave6_async_n20_nested": {
        "folder": "async_vs_sync_dll",
        "rubric": (
            "Total 4 marks:\n"
            "1) Framing difference (async start/stop + sync frames/SYN/flag) (2 marks)\n"
            "2) Trade-offs (rates / complexity / synchronization) (2 marks)"
        ),
        "rubric_items": [
            {
                "rubric_item_id": "R1",
                "label": "Framing difference",
                "marks": 2.0,
                "atomic": False,
                "description": "MAY SPLIT into async framing + sync framing.",
            },
            {
                "rubric_item_id": "R2",
                "label": "Trade-offs",
                "marks": 2.0,
                "atomic": False,
                "description": "MAY SPLIT into async trade-off + sync trade-off.",
            },
        ],
        "concept_to_rubric": {
            "Q1_C1": "R1",  # async framing
            "Q1_C3": "R1",  # sync framing
            "Q1_C2": "R2",  # async trade-off
            "Q1_C4": "R2",  # sync trade-off
        },
        # Framing required; trade-offs optional (matches Wave6 human gold)
        "default_required": {"R1": True, "R2": False},
    },
    "e2e_wave6_conn_n20_nested": {
        "folder": "conn_oriented_vs_less",
        "rubric": (
            "Total 5 marks:\n"
            "1) Chooses connectionless (1 mark)\n"
            "2) Reasoning for the choice (many partners / short interactions / overhead) (4 marks)"
        ),
        "rubric_items": [
            {
                "rubric_item_id": "R1",
                "label": "Chooses connectionless",
                "marks": 1.0,
                "atomic": True,
                "description": "Do not subdivide — the choice itself.",
            },
            {
                "rubric_item_id": "R2",
                "label": "Reasoning for the choice",
                "marks": 4.0,
                "atomic": False,
                "description": "MAY SPLIT into partners / short interactions / overhead arguments.",
            },
        ],
        "concept_to_rubric": {
            "Q1_C1": "R1",
            "Q1_C2": "R2",
            "Q1_C3": "R2",
            "Q1_C4": "R2",
        },
        "default_required": {"R1": True, "R2": True},
    },
    "e2e_wave6_dll3_n20_nested": {
        "folder": "dll_service_classes",
        "rubric": (
            "Total 3 marks:\n"
            "1) Three DLL service classes named and distinguished (3 marks)"
        ),
        "rubric_items": [
            {
                "rubric_item_id": "R1",
                "label": "Three DLL service classes named and distinguished",
                "marks": 3.0,
                "atomic": False,
                "description": "MAY SPLIT into the three service classes.",
            },
        ],
        "concept_to_rubric": {
            "Q1_C1": "R1",
            "Q1_C2": "R1",
            "Q1_C3": "R1",
        },
        "default_required": {"R1": True},
    },
    # BURST already nested correctly — only refresh pack copy from exam store if needed
    "e2e_wave6_burst_n20_nested": {
        "folder": "frame_bursting",
        "rubric": (
            "Total 3 marks:\n"
            "1) Definition of frame bursting (1.5 marks)\n"
            "2) Advantage and disadvantage vs carrier extension (1.5 marks)"
        ),
        "rubric_items": [
            {
                "rubric_item_id": "R1",
                "label": "Definition of frame bursting",
                "marks": 1.5,
                "atomic": True,
                "description": "Do not subdivide.",
            },
            {
                "rubric_item_id": "R2",
                "label": "Advantage and disadvantage vs carrier extension",
                "marks": 1.5,
                "atomic": False,
                "description": "MAY SPLIT into advantage + disadvantage.",
            },
        ],
        "concept_to_rubric": {
            "Q1_C1": "R1",
            "Q1_C2": "R2",
            "Q1_C3": "R2",
        },
        "default_required": {"R1": True, "R2": True},
    },
}


def _write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  wrote {path.relative_to(PROJECT)}")


def apply_exam(exam_id: str, spec: dict) -> None:
    exam_dir = PROJECT / "data" / "exams" / exam_id
    cfg_path = exam_dir / "exam_config.json"
    cqa_path = exam_dir / "cqa_tuples.json"
    if not cfg_path.exists() or not cqa_path.exists():
        print(f"skip {exam_id}: missing store files")
        return

    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    q = cfg["exam"]["questions"][0]
    q["rubric"] = spec["rubric"]
    q["rubric_items"] = spec["rubric_items"]
    _write(cfg_path, cfg)

    cqa_doc = json.loads(cqa_path.read_text(encoding="utf-8"))
    mapping = spec["concept_to_rubric"]
    for c in cqa_doc["cqa_tuples"]:
        cid = c["concept_id"]
        if cid not in mapping:
            raise SystemExit(f"{exam_id}: unexpected concept {cid}")
        c["rubric_item_id"] = mapping[cid]
    _write(cqa_path, cqa_doc)

    # Reset teacher calibration to new rubric shape
    by_rubric: dict[str, list[str]] = {}
    for cid, rid in mapping.items():
        by_rubric.setdefault(rid, []).append(cid)
    cal = {
        "exam_id": exam_id,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "rubrics": [
            {
                "rubric_item_id": rid,
                "required_for_full_marks": bool(spec["default_required"].get(rid, True)),
                "concepts": [
                    {
                        "concept_id": cid,
                        "needed_for_rubric": True,
                        "partial_credit_note": "",
                        "matching_note": "",
                    }
                    for cid in sorted(by_rubric.get(rid, []))
                ],
            }
            for rid in [ri["rubric_item_id"] for ri in spec["rubric_items"]]
        ],
    }
    _write(exam_dir / "teacher_calibration.json", cal)

    # Keep pack exam_nested.json in sync
    pack_path = PACK / spec["folder"] / "exam_nested.json"
    if pack_path.exists():
        pack = json.loads(pack_path.read_text(encoding="utf-8"))
        pq = pack["exam"]["questions"][0]
        pq["rubric"] = spec["rubric"]
        pq["rubric_items"] = spec["rubric_items"]
        _write(pack_path, pack)

    # Sanity: concept marks under each bucket sum to bucket marks
    marks_by: dict[str, float] = {}
    for c in cqa_doc["cqa_tuples"]:
        marks_by[c["rubric_item_id"]] = marks_by.get(c["rubric_item_id"], 0.0) + float(c["marks"])
    for ri in spec["rubric_items"]:
        got = marks_by.get(ri["rubric_item_id"], 0.0)
        if abs(got - float(ri["marks"])) > 1e-6:
            raise SystemExit(
                f"{exam_id}: {ri['rubric_item_id']} marks {ri['marks']} != concepts sum {got}"
            )
    print(f"ok {exam_id}: " + ", ".join(f"{k}={v}" for k, v in sorted(marks_by.items())))


def main() -> None:
    for exam_id, spec in REMAP.items():
        print(f"\n== {exam_id}")
        apply_exam(exam_id, spec)


if __name__ == "__main__":
    main()
