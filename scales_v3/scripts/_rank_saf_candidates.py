"""Rank SAF (ASAG2024) questions for SCALES-style concept grading fit."""

from __future__ import annotations

import json
from pathlib import Path

import pyarrow.parquet as pq

CACHE = Path(
    r"C:\Users\manav\.cache\huggingface\hub\datasets--Meyerger--ASAG2024"
    r"\snapshots\9a7a179de4e227f5e78625bc9ded2d8761f1ff09\train.parquet"
)
OUT = Path("data/e2e_eval/wave5_real/_saf_candidates.json")


def main() -> None:
    df = pq.read_table(CACHE).to_pandas()
    saf = df[df["data_source"] == "SAF"].copy()

    out = []
    for q, g in saf.groupby("question"):
        ref = str(g["reference_answer"].iloc[0])
        grades = g["normalized_grade"].astype(float)
        lens = g["provided_answer"].astype(str).str.len()
        high = int((grades >= 0.75).sum())
        mid = int(((grades >= 0.4) & (grades < 0.75)).sum())
        low = int((grades < 0.4).sum())
        qlow = q.lower()
        rlow = ref.lower()
        score = 0
        for kw in (
            "tcp",
            "congestion",
            "ip",
            "routing",
            "duplicate",
            "connection",
            "mac",
            "aloha",
            "csma",
            "class a",
            "slow start",
            "transport",
        ):
            if kw in qlow or kw in rlow:
                score += 1
        if any(x in qlow for x in ("2 ", "two ", "3 ", "three ", "name the", "list", "methods")):
            score += 2
        if len(ref) > 100:
            score += 1
        if float(lens.median()) > 150:
            score += 1
        if high >= 2 and mid >= 2 and low >= 2:
            score += 2  # usable band mix

        idxs = [0, len(g) // 2, len(g) - 1]
        samples = []
        sorted_g = g.sort_values("normalized_grade")
        for i in idxs:
            r = sorted_g.iloc[i]
            samples.append(
                {
                    "grade": float(r["normalized_grade"]),
                    "ans": str(r["provided_answer"])[:500],
                }
            )

        out.append(
            {
                "fit": score,
                "n": int(len(g)),
                "high": high,
                "mid": mid,
                "low": low,
                "grade_mean": round(float(grades.mean()), 2),
                "ans_med": int(lens.median()),
                "ref_len": len(ref),
                "q": q,
                "ref": ref,
                "samples": samples,
            }
        )

    out.sort(key=lambda x: (-x["fit"], -x["n"]))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out[:10], indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {OUT}")
    for o in out[:10]:
        print(
            f"fit={o['fit']} n={o['n']} H/M/L={o['high']}/{o['mid']}/{o['low']} "
            f"med_len={o['ans_med']}"
        )
        print(" ", o["q"][:160].replace("\n", " "))
        print()


if __name__ == "__main__":
    main()
