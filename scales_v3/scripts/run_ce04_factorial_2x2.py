#!/usr/bin/env python3
"""CE04 2x2 factorial: facets present/absent × criteria strict/holistic.

Arms:
  A1 — facets present + strict criteria (current corrected select_n C1)
  A2 — facets absent (skip_facets) + strict criteria
  A3 — facets present + holistic criteria (synonym_set, optional synonym facets)
  A4 — facets absent + holistic criteria (= prior Exp A)

Same first N students from student_smoke_n10/CE04_grades.json.
"""

from __future__ import annotations

import asyncio
import copy
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
STRICT_PACK = PROJECT / "data/cera_eval/runs/cera_eval_v1_corrected/CE04.json"
HOLISTIC_PACK = PROJECT / "data/cera_eval/runs/ce04_nofacets_n8/CE04_nofacets.json"
OUT = PROJECT / "data/cera_eval/runs/ce04_factorial_2x2"
N = 8


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


def build_a3_pack(holistic: dict, strict: dict) -> dict:
    """Holistic criteria + synonym facets present (not select_n)."""
    pack = copy.deepcopy(holistic)
    pack["mode"] = "holistic_criteria_with_synonym_facets"
    # C1: keep holistic criteria/role; add optional synonym phrasings (NOT channel-hold as separate required)
    c1 = pack["cqa_tuples"][0]
    c1["evidence_facets"] = [
        "multiple frames concatenated / sent together in one burst",
        "collecting several frames and transmitting them at once",
    ]
    c1["evidence_role"] = "synonym_set"
    c1["min_count"] = None
    c1["expected_keywords"] = ["concatenat", "multiple", "frames", "burst", "together"]
    c1["acceptable_variants"] = [
        "sending several frames at once",
        "grouping frames into one transmission",
        "combining frames into a single burst",
    ]
    # C2/C3: holistic criteria from Exp A + synonym facets from strict pack
    for i, cid in enumerate(("CE04_C2", "CE04_C3"), start=1):
        h = pack["cqa_tuples"][i]
        s = next(c for c in strict["cqa_tuples"] if c["concept_id"] == cid)
        h["evidence_facets"] = list(s.get("evidence_facets") or [])
        h["expected_keywords"] = list(s.get("expected_keywords") or [])
        h["acceptable_variants"] = list(s.get("acceptable_variants") or [])
        h["evidence_role"] = "synonym_set"
        h["min_count"] = None
    return pack


async def grade_arm(
    arm_id: str,
    pack: dict,
    students: list[dict],
    df: pd.DataFrame,
    skip_facets: bool,
) -> dict:
    total = float(pack["total_marks"])
    cqas = [CQATuple.model_validate(c) for c in pack["cqa_tuples"]]
    settings = get_settings()
    cgr = CGRModule(LLMClient(settings.llm), settings, skip_facets=skip_facets)

    rows = []
    for s in students:
        ans, human, norm = match_ans(df, s["answer_preview"], total)
        if ans is None:
            print(f"  SKIP {s['student_id']}")
            continue
        sid = s["student_id"]
        print(f"  {arm_id} {sid} human={human}")
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
                    "verdict": r.verdict.value,
                    "marks_awarded": r.marks_awarded,
                    "max_marks": cqa.marks,
                    "evidence_span": r.evidence_span,
                    "reasoning": r.reasoning,
                }
            )
            sys_marks += r.marks_awarded
            print(
                f"    {r.concept_id}: {r.verdict.value} {r.marks_awarded:g} "
                f"{(r.evidence_span or '')[:55]!r}"
            )
        bias = sys_marks - human
        rows.append(
            {
                "student_id": sid,
                "human_norm": norm,
                "human_est_marks": human,
                "system_marks": sys_marks,
                "abs_err": abs(bias),
                "bias": bias,
                "answer": ans,
                "concepts": concepts,
            }
        )

    n = len(rows)
    mae = sum(r["abs_err"] for r in rows) / n if n else None
    mean_bias = sum(r["bias"] for r in rows) / n if n else None
    over = sum(1 for r in rows if r["bias"] > 0.01)
    under = sum(1 for r in rows if r["bias"] < -0.01)
    exact = n - over - under
    return {
        "arm_id": arm_id,
        "skip_facets": skip_facets,
        "n_students": n,
        "mae": round(mae, 3) if mae is not None else None,
        "mean_bias": round(mean_bias, 3) if mean_bias is not None else None,
        "n_over": over,
        "n_under": under,
        "n_exact": exact,
        "students": rows,
    }


async def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    strict = json.loads(STRICT_PACK.read_text(encoding="utf-8"))
    holistic = json.loads(HOLISTIC_PACK.read_text(encoding="utf-8"))
    a3 = build_a3_pack(holistic, strict)

    (OUT / "pack_A1_strict_facets.json").write_text(
        json.dumps(strict, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (OUT / "pack_A3_holistic_with_facets.json").write_text(
        json.dumps(a3, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (OUT / "pack_A4_holistic_nofacets.json").write_text(
        json.dumps(holistic, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    smoke = json.loads(SMOKE.read_text(encoding="utf-8"))
    students = smoke["students"][:N]
    df = pd.read_parquet(SRC)

    arms_spec = [
        ("A1", strict, False, "facets present + strict select_n criteria"),
        ("A2", strict, True, "facets absent + strict criteria"),
        ("A3", a3, False, "facets present + holistic criteria"),
        ("A4", holistic, True, "facets absent + holistic criteria"),
    ]

    arm_results = []
    for arm_id, pack, skip, desc in arms_spec:
        print(f"\n===== {arm_id}: {desc} =====")
        res = await grade_arm(arm_id, pack, students, df, skip_facets=skip)
        res["description"] = desc
        (OUT / f"{arm_id}_grades.json").write_text(
            json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        arm_results.append(res)
        print(
            f"  MAE={res['mae']}  mean_bias={res['mean_bias']:+}  "
            f"exact={res['n_exact']} over={res['n_over']} under={res['n_under']}"
        )

    by_id = {a["arm_id"]: a for a in arm_results}
    a1, a2, a3r, a4 = by_id["A1"], by_id["A2"], by_id["A3"], by_id["A4"]
    summary = {
        "run_ts": datetime.now(UTC).isoformat(),
        "n_students": N,
        "design": "2x2 facets×criteria on CE04",
        "arms": [
            {
                "arm_id": a["arm_id"],
                "description": a["description"],
                "skip_facets": a["skip_facets"],
                "mae": a["mae"],
                "mean_bias": a["mean_bias"],
                "n_exact": a["n_exact"],
                "n_over": a["n_over"],
                "n_under": a["n_under"],
            }
            for a in arm_results
        ],
        "contrasts": {
            "A1_vs_A2_facet_blank_under_strict": round((a2["mae"] or 0) - (a1["mae"] or 0), 3),
            "A1_vs_A3_criteria_rewrite_with_facets": round((a3r["mae"] or 0) - (a1["mae"] or 0), 3),
            "A2_vs_A4_criteria_rewrite_without_facets": round(
                (a4["mae"] or 0) - (a2["mae"] or 0), 3
            ),
            "A3_vs_A4_facet_blank_under_holistic": round((a4["mae"] or 0) - (a3r["mae"] or 0), 3),
        },
        "interpretation_hint": (
            "Negative contrast = second arm better (lower MAE). "
            "If |A1_vs_A3| >> |A1_vs_A2|, criteria rewrite dominates."
        ),
    }
    winner = min(arm_results, key=lambda a: a["mae"] if a["mae"] is not None else 9e9)
    summary["winning_arm"] = winner["arm_id"]
    summary["winning_mae"] = winner["mae"]
    (OUT / "SUMMARY.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    lines = [
        "# CE04 2×2 factorial — facets × criteria",
        "",
        f"n={N} same smoke students. Run: {summary['run_ts']}",
        "",
        "| Arm | Facets | Criteria | MAE | mean bias (sys−hum) | exact | over | under |",
        "|---|---|---|---:|---:|---:|---:|---:|",
    ]
    for a in arm_results:
        facets = "absent" if a["skip_facets"] else "present"
        crit = "holistic" if a["arm_id"] in ("A3", "A4") else "strict"
        lines.append(
            f"| {a['arm_id']} | {facets} | {crit} | {a['mae']} | "
            f"{a['mean_bias']:+} | {a['n_exact']} | {a['n_over']} | {a['n_under']} |"
        )
    lines += [
        "",
        "## Contrasts (Δ MAE = armB − armA; negative = B better)",
        "",
        "```json",
        json.dumps(summary["contrasts"], indent=2),
        "```",
        "",
        f"**Winning arm:** {summary['winning_arm']} (MAE {summary['winning_mae']})",
        "",
    ]
    for a in arm_results:
        lines += ["=" * 72, "", f"## {a['arm_id']} — {a['description']}", ""]
        for r in a["students"]:
            lines += [
                "-" * 40,
                f"### {r['student_id']}  H={r['human_est_marks']:g}  "
                f"S={r['system_marks']:g}  bias={r['bias']:+g}",
                "",
                "| Concept | Verdict | Marks | Evidence |",
                "|---|---|---:|---|",
            ]
            for c in r["concepts"]:
                evid = (c["evidence_span"] or "—").replace("|", "\\|").replace("\n", " ")
                if len(evid) > 200:
                    evid = evid[:197] + "…"
                lines.append(
                    f"| `{c['concept_id']}` | {c['verdict']} | "
                    f"{c['marks_awarded']:g}/{c['max_marks']:g} | {evid} |"
                )
            lines.append("")

    (OUT / "ANALYSIS.md").write_text("\n".join(lines), encoding="utf-8")
    print("\nSUMMARY", json.dumps(summary, indent=2))
    print("Wrote", OUT)


if __name__ == "__main__":
    asyncio.run(main())
