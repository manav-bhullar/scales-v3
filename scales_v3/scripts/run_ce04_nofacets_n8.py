#!/usr/bin/env python3
"""Grade CE04 on 8 students with empty evidence facets (criteria-only)."""

from __future__ import annotations

import asyncio
import json
import re
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

from scales.config import get_settings
from scales.models.cqa import CQATuple
from scales.modules.cgr import CGRModule
from scales.services.llm_client import LLMClient

PROJECT = Path(__file__).resolve().parents[1]
SRC = PROJECT / (
    "data/e2e_eval/wave5_real/saf_wave6_picked/wave6_coarse_n20/frame_bursting/source.parquet"
)
SMOKE = PROJECT / "data/cera_eval/runs/student_smoke_n10/CE04_grades.json"
OUT = PROJECT / "data/cera_eval/runs/ce04_nofacets_n8"
N = 8


def build_nofacet_pack() -> dict:
    """Criteria-only CQAs: empty facets/variants/keywords; synonym_set everywhere."""
    now = datetime.now(UTC).isoformat()
    return {
        "id": "CE04",
        "question_text": (
            'What is "frame bursting"? Also, give 1 advantage and disadvantage '
            "compared to the carrier extension."
        ),
        "reference_answer": (
            "Frame bursting reduces the overhead for transmitting small frames by "
            "concatenating a sequence of multiple frames in one single transmission, "
            "without ever releasing control of the channel.\n"
            "Advantage: it is more efficient than carrier extension as single frames "
            "not filled up with garbage.\n"
            "Disadvantage: need frames waiting for transmission or buffering and delay "
            "of frames"
        ),
        "rubric": (
            "Total 3 marks:\n"
            "1) Definition of frame bursting (1 mark)\n"
            "2) One advantage compared to carrier extension (1 mark)\n"
            "3) One disadvantage compared to carrier extension (1 mark)"
        ),
        "total_marks": 3,
        "marks_sum": 3.0,
        "concept_count": 3,
        "mode": "no_facets_criteria_only",
        "cqa_tuples": [
            {
                "concept_id": "CE04_C1",
                "question_id": "CE04",
                "knowledge_point": (
                    "Define frame bursting as sending multiple frames together "
                    "in one burst/transmission."
                ),
                "target_criteria": (
                    "FULL if the student states that multiple frames are "
                    "concatenated / collected / sent together in one transmission "
                    "or burst. Channel-hold / 'without releasing the channel' is "
                    "NOT required separately — it is implied by one burst. "
                    "PARTIAL if they only vaguely mention bursting or larger frames "
                    "without multiple-frames-together. ABSENT if definition missing."
                ),
                "marks": 1.0,
                "rubric_item_id": "1",
                "evidence_facets": [],
                "evidence_role": "synonym_set",
                "min_count": None,
                "evidence_mode": "ANY",
                "expected_keywords": [],
                "acceptable_variants": [],
                "partial_credit_rule": ("0.5 if only a vague / incomplete definition of bursting"),
                "source_rubric_span": "Definition of frame bursting (1 mark)",
                "source_reference_span": (
                    "concatenating a sequence of multiple frames in one single transmission"
                ),
                "version": 1,
                "created_at": now,
                "updated_at": now,
            },
            {
                "concept_id": "CE04_C2",
                "question_id": "CE04",
                "knowledge_point": (
                    "Advantage of frame bursting vs carrier extension: efficiency / throughput."
                ),
                "target_criteria": (
                    "FULL if student states an efficiency / throughput / performance / "
                    "user-data advantage (vs carrier extension or in general). "
                    "Accept paraphrases and typos (efficency). ABSENT if no advantage."
                ),
                "marks": 1.0,
                "rubric_item_id": "2",
                "evidence_facets": [],
                "evidence_role": "synonym_set",
                "min_count": None,
                "evidence_mode": "ANY",
                "expected_keywords": [],
                "acceptable_variants": [],
                "partial_credit_rule": None,
                "source_rubric_span": ("One advantage compared to carrier extension (1 mark)"),
                "source_reference_span": (
                    "more efficient than carrier extension as single frames not "
                    "filled up with garbage"
                ),
                "version": 1,
                "created_at": now,
                "updated_at": now,
            },
            {
                "concept_id": "CE04_C3",
                "question_id": "CE04",
                "knowledge_point": ("Disadvantage of frame bursting: waiting / buffering / delay."),
                "target_criteria": (
                    "FULL if student states frames must wait / be buffered, or that "
                    "bursting causes delay / latency. ABSENT if no disadvantage."
                ),
                "marks": 1.0,
                "rubric_item_id": "3",
                "evidence_facets": [],
                "evidence_role": "synonym_set",
                "min_count": None,
                "evidence_mode": "ANY",
                "expected_keywords": [],
                "acceptable_variants": [],
                "partial_credit_rule": None,
                "source_rubric_span": ("One disadvantage compared to carrier extension (1 mark)"),
                "source_reference_span": (
                    "need frames waiting for transmission or buffering and delay of frames"
                ),
                "version": 1,
                "created_at": now,
                "updated_at": now,
            },
        ],
    }


def match_ans(df: pd.DataFrame, preview: str, total: float):
    hits = df[df["provided_answer"].astype(str).str.startswith(preview[:50].rstrip(), na=False)]
    if len(hits) == 0:
        key = re.sub(r"\s+", " ", preview[:55])
        for _, row in df.iterrows():
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


async def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    pack = build_nofacet_pack()
    (OUT / "CE04_nofacets.json").write_text(
        json.dumps(pack, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    smoke = json.loads(SMOKE.read_text(encoding="utf-8"))
    df = pd.read_parquet(SRC)
    total = float(pack["total_marks"])
    cqas = [CQATuple.model_validate(c) for c in pack["cqa_tuples"]]

    # Reuse first 8 smoke students for direct vs-facet comparison
    selected = smoke["students"][:N]
    settings = get_settings()
    cgr = CGRModule(LLMClient(settings.llm), settings)

    rows = []
    for s in selected:
        ans, human, norm = match_ans(df, s["answer_preview"], total)
        if ans is None:
            print("SKIP no match", s["student_id"])
            continue
        sid = s["student_id"]
        print(f"\n=== {sid} human={human}")
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
                    "role": cqa.evidence_role,
                    "min_count": cqa.min_count,
                    "max_marks": cqa.marks,
                    "verdict": r.verdict.value,
                    "marks_awarded": r.marks_awarded,
                    "evidence_span": r.evidence_span,
                    "reasoning": r.reasoning,
                }
            )
            sys_marks += r.marks_awarded
            print(
                f"  {r.concept_id}: {r.verdict.value} {r.marks_awarded} "
                f"evid={r.evidence_span[:70]!r}"
            )

        # facet-based system marks from prior smoke (same student)
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

    mae_nf = sum(r["abs_err_nofacets"] for r in rows) / len(rows)
    mae_f = sum(r["abs_err_with_facets"] for r in rows) / len(rows)
    out = {
        "question_id": "CE04",
        "mode": "no_facets_criteria_only",
        "n_students": len(rows),
        "total_marks": total,
        "mae_nofacets": round(mae_nf, 3),
        "mae_with_facets_same_students": round(mae_f, 3),
        "run_ts": datetime.now(UTC).isoformat(),
        "students": rows,
    }
    (OUT / "grades.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Flat ANALYSIS.md
    lines = [
        "# CE04 — no-facets criteria-only (n=8)",
        "",
        "Empty `evidence_facets` / keywords / variants. CGR falls back to Target Criteria.",
        "C1 is `synonym_set` (not select_n): channel-hold not required separately.",
        "",
        f"**MAE no-facets:** {mae_nf:.3f}  ·  **MAE with-facets (same 8):** {mae_f:.3f}",
        "",
    ]
    for r in rows:
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
            f"| System (with facets, prior smoke) | {r['system_marks_with_facets']:g} / {total:g} |",
            rf"| \|err\| no-facets | {r['abs_err_nofacets']:g} |",
            "",
            "**Student answer**",
            "",
            "```",
            r["answer"].strip(),
            "```",
            "",
            "**Our check (no facets)**",
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

    (OUT / "ANALYSIS.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"\nMAE no-facets={mae_nf:.3f}  with-facets={mae_f:.3f}")
    print("wrote", OUT)


if __name__ == "__main__":
    asyncio.run(main())
