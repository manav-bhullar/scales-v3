#!/usr/bin/env python3
"""Fix CERA modes/rubrics for CE06–CE10, stamp roles on others, write corrected pack."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "data" / "cera_eval" / "runs"
NOW = datetime.now(timezone.utc).isoformat()


def load(qid: str, prefer: tuple[str, ...] = ("cera_eval_v1_roles", "cera_eval_v1_iter", "cera_eval_v1")):
    for d in prefer:
        p = ROOT / d / f"{qid}.json"
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8")), p
    raise FileNotFoundError(qid)


def save(qid: str, data: dict, *dirs: str) -> None:
    data["marks_sum"] = sum(float(c["marks"]) for c in data["cqa_tuples"])
    data["concept_count"] = len(data["cqa_tuples"])
    data["corrected_ts"] = NOW
    text = json.dumps(data, indent=2, ensure_ascii=False)
    for d in dirs:
        out = ROOT / d
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{qid}.json").write_text(text, encoding="utf-8")


def main() -> None:
    # CE06
    data, _ = load("CE06")
    for c in data["cqa_tuples"]:
        if c["concept_id"] == "CE06_C1":
            c.update(
                {
                    "evidence_role": "select_n",
                    "min_count": 2,
                    "evidence_mode": "ANY",
                    "target_criteria": (
                        "FULL = at least 2 of 3 definition parts "
                        "(network management protocol / dynamically assigns IP / "
                        "configures parameters); PARTIAL = exactly 1; ABSENT = 0"
                    ),
                    "partial_credit_rule": "exactly 1 definition part → 1.0 mark",
                    "updated_at": NOW,
                }
            )
        if c["concept_id"] == "CE06_C2":
            c.update(
                {
                    "evidence_role": "select_n",
                    "min_count": 2,
                    "evidence_mode": "ANY",
                    "target_criteria": (
                        "FULL = at least 2 distinct uses from the catalog; "
                        "PARTIAL = exactly 1; ABSENT = 0"
                    ),
                    "partial_credit_rule": "exactly 1 use → 1.0 mark",
                    "updated_at": NOW,
                }
            )
    save("CE06", data, "cera_eval_v1", "cera_eval_v1_corrected")

    # CE07
    data, _ = load("CE07")
    for c in data["cqa_tuples"]:
        if c["concept_id"] == "CE07_C1":
            c.update(
                {
                    "evidence_role": "select_n",
                    "min_count": 2,
                    "evidence_mode": "ANY",
                    "target_criteria": (
                        "FULL = at least 2 parts (extend fixed header / "
                        "optional network-layer info); PARTIAL = exactly 1; ABSENT = 0"
                    ),
                    "partial_credit_rule": "exactly 1 part → 0.75 marks",
                    "updated_at": NOW,
                }
            )
        if c["concept_id"] == "CE07_C2":
            c.update(
                {
                    "evidence_role": "synonym_set",
                    "min_count": None,
                    "evidence_mode": "ANY",
                    "target_criteria": (
                        "any of: between fixed header and payload / "
                        "between main header and upper-layer or transport header"
                    ),
                    "partial_credit_rule": None,
                    "updated_at": NOW,
                }
            )
        if c["concept_id"] == "CE07_C3":
            # Reference: ONE of the two advantages is fully correct
            c.update(
                {
                    "evidence_role": "synonym_set",
                    "min_count": None,
                    "evidence_mode": "ANY",
                    "target_criteria": (
                        "any of: appending new options without changing header / "
                        "faster processing by intermediate devices "
                        "(ONE advantage is FULL)"
                    ),
                    "partial_credit_rule": None,
                    "updated_at": NOW,
                }
            )
    save("CE07", data, "cera_eval_v1", "cera_eval_v1_corrected")

    # CE08: name any 4
    data, _ = load("CE08")
    data["rubric"] = (
        "Total 4 marks:\n"
        "1) Naming any 4 valid challenges (1 mark). Catalog: Adaptation, Security, "
        "MAC, QoS, Scalability, Power.\n"
        "2) Describing challenge A (1.5 marks)\n"
        "3) Describing challenge B (1.5 marks)"
    )
    for c in data["cqa_tuples"]:
        if c["concept_id"].endswith("_C1"):
            c.update(
                {
                    "knowledge_point": (
                        "The student names at least four distinct mobile routing "
                        "challenges from the catalog."
                    ),
                    "evidence_role": "select_n",
                    "min_count": 4,
                    "evidence_mode": "ANY",
                    "target_criteria": (
                        "FULL = at least 4 distinct valid challenges named; "
                        "PARTIAL = 1..3; ABSENT = 0"
                    ),
                    "partial_credit_rule": "1–3 valid names → 0.5 marks",
                    "updated_at": NOW,
                }
            )
        elif c["concept_id"].endswith(("_C2", "_C3")):
            c.update(
                {
                    "evidence_role": "synonym_set",
                    "min_count": None,
                    "evidence_mode": "ANY",
                    "updated_at": NOW,
                }
            )
    save(
        "CE08",
        data,
        "cera_eval_v1",
        "cera_eval_v1_roles",
        "cera_eval_v1_iter",
        "cera_eval_v1_corrected",
    )

    # CE09
    data, _ = load("CE09")
    for c in data["cqa_tuples"]:
        if c["concept_id"] == "CE09_C1":
            c.update(
                {
                    "evidence_role": "select_n",
                    "min_count": 2,
                    "evidence_mode": "ANY",
                    "target_criteria": (
                        "FULL = at least 2 distinct benefits from the catalog; "
                        "PARTIAL = exactly 1; ABSENT = 0"
                    ),
                    "partial_credit_rule": "exactly 1 benefit → 1.0 mark",
                    "updated_at": NOW,
                }
            )
        if c["concept_id"] == "CE09_C2":
            c.update(
                {
                    "evidence_role": "select_n",
                    "min_count": 2,
                    "evidence_mode": "ANY",
                    "target_criteria": (
                        "FULL = at least 2 distinct drawbacks from the catalog; "
                        "PARTIAL = exactly 1; ABSENT = 0"
                    ),
                    "partial_credit_rule": "exactly 1 drawback → 1.0 mark",
                    "updated_at": NOW,
                }
            )
    save("CE09", data, "cera_eval_v1", "cera_eval_v1_corrected")

    # CE10
    data, _ = load("CE10", prefer=("cera_eval_v1_iter", "cera_eval_v1"))
    data["total_marks"] = 5
    data["rubric"] = (
        "Total 5 marks:\n"
        "1) Naming the 2 phases (1 mark)\n"
        "2) Explaining cwnd/ss_thresh in Slow Start (2 marks)\n"
        "3) Explaining cwnd/ss_thresh in Congestion Avoidance (2 marks)"
    )
    for c in data["cqa_tuples"]:
        if c["concept_id"].endswith("_C1"):
            c.update(
                {
                    "marks": 1.0,
                    "evidence_role": "checklist",
                    "min_count": None,
                    "evidence_mode": "ALL",
                    "target_criteria": (
                        "FULL requires naming both Slow Start and Congestion Avoidance"
                    ),
                    "partial_credit_rule": "naming only one phase → 0.5 marks",
                    "source_rubric_span": "Naming the 2 phases (1 mark)",
                    "updated_at": NOW,
                }
            )
        if c["concept_id"].endswith("_C2"):
            c.update(
                {
                    "marks": 2.0,
                    "evidence_role": "synonym_set",
                    "min_count": None,
                    "evidence_mode": "ANY",
                    "target_criteria": (
                        "any of: cwnd +1 per ACK / doubles each RTT / exponential growth"
                    ),
                    "partial_credit_rule": "vague growth without mechanism → 1.0 mark",
                    "source_rubric_span": "Explaining Slow Start (2 marks)",
                    "updated_at": NOW,
                }
            )
        if c["concept_id"].endswith("_C3"):
            c.update(
                {
                    "marks": 2.0,
                    "evidence_role": "synonym_set",
                    "min_count": None,
                    "evidence_mode": "ANY",
                    "target_criteria": (
                        "any of: linear growth of cwnd / +1 after all segments ACKed"
                    ),
                    "partial_credit_rule": "vague growth without mechanism → 1.0 mark",
                    "source_rubric_span": "Explaining Congestion Avoidance (2 marks)",
                    "updated_at": NOW,
                }
            )
    save("CE10", data, "cera_eval_v1", "cera_eval_v1_iter", "cera_eval_v1_corrected")

    # CE04 already fixed; stamp into corrected
    data, _ = load("CE04")
    save("CE04", data, "cera_eval_v1_corrected")

    for qid in ["CE01", "CE02", "CE03", "CE05"]:
        data, _ = load(qid)
        for c in data["cqa_tuples"]:
            if not c.get("evidence_role"):
                c["evidence_role"] = (
                    "checklist" if c.get("evidence_mode") == "ALL" else "synonym_set"
                )
                c["min_count"] = None
        save(qid, data, "cera_eval_v1_corrected")

    print("OK corrected pack")
    for p in sorted((ROOT / "cera_eval_v1_corrected").glob("CE*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        print(f"{p.name} marks={d['marks_sum']} n={d['concept_count']}")
        for c in d["cqa_tuples"]:
            print(
                f"  {c['concept_id']} {c['marks']} "
                f"role={c.get('evidence_role')} min={c.get('min_count')}"
            )


if __name__ == "__main__":
    main()
