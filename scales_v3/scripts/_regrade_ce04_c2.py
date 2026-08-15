#!/usr/bin/env python3
"""Re-grade CE04_C2 ABSENT students after broadening efficiency paraphrases."""

from __future__ import annotations

import asyncio
import json
import re
from pathlib import Path

import pandas as pd

from scales.config import get_settings
from scales.models.cqa import CQATuple
from scales.modules.cgr import CGRModule
from scales.services.llm_client import LLMClient

OUT = Path("data/cera_eval/runs/student_smoke_n10")
PACK = Path("data/cera_eval/runs/cera_eval_v1_corrected/CE04.json")
SRC = Path(
    "data/e2e_eval/wave5_real/saf_wave6_picked/wave6_coarse_n20/frame_bursting/source.parquet"
)


def match_ans(df: pd.DataFrame, preview: str, total: float):
    hits = df[df["provided_answer"].astype(str).str.startswith(preview[:50].rstrip(), na=False)]
    if len(hits) == 0:
        key = re.sub(r"\s+", " ", preview[:55])
        for i, row in df.iterrows():
            if key[:35] in re.sub(r"\s+", " ", str(row["provided_answer"])):
                return str(row["provided_answer"]), float(row["normalized_grade"]) * total
        return None, None
    r = hits.iloc[0]
    return str(r["provided_answer"]), float(r["normalized_grade"]) * total


async def main() -> None:
    pack = json.loads(PACK.read_text(encoding="utf-8"))
    grades = json.loads((OUT / "CE04_grades.json").read_text(encoding="utf-8"))
    df = pd.read_parquet(SRC)
    total = float(pack["total_marks"])
    c2 = CQATuple.model_validate(
        next(c for c in pack["cqa_tuples"] if c["concept_id"] == "CE04_C2")
    )
    targets = [
        s
        for s in grades["students"]
        if any(c["concept_id"] == "CE04_C2" and c["verdict"] == "ABSENT" for c in s["concepts"])
    ]
    print("targets", [s["student_id"] for s in targets])

    settings = get_settings()
    cgr = CGRModule(LLMClient(settings.llm), settings)

    for s in targets:
        ans, human = match_ans(df, s["answer_preview"], total)
        assert ans is not None
        print(f"\n=== {s['student_id']} human={human}")
        print(ans[:400].replace("\n", " "))
        r = await cgr.grade_concept(s["student_id"], ans, c2, pack["question_text"])
        print(f"C2 -> {r.verdict.value} {r.marks_awarded} evid={r.evidence_span!r}")
        print("reason:", r.reasoning[:240])
        for c in s["concepts"]:
            if c["concept_id"] == "CE04_C2":
                c["verdict"] = r.verdict.value
                c["marks_awarded"] = r.marks_awarded
                c["evidence_span"] = r.evidence_span
        s["system_marks"] = sum(c["marks_awarded"] for c in s["concepts"])
        if human is not None:
            s["human_est_marks"] = human
        s["abs_err"] = abs(s["system_marks"] - s["human_est_marks"])
        s["answer_preview"] = ans[:160]

    grades["mae"] = sum(st["abs_err"] for st in grades["students"]) / len(grades["students"])
    (OUT / "CE04_grades.json").write_text(
        json.dumps(grades, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print("\nCE04 MAE now", grades["mae"])
    for st in grades["students"]:
        c2v = next(c for c in st["concepts"] if c["concept_id"] == "CE04_C2")
        print(
            f"{st['student_id']}: H={st['human_est_marks']} S={st['system_marks']} "
            f"C2={c2v['verdict']}({c2v['marks_awarded']})"
        )


if __name__ == "__main__":
    asyncio.run(main())
