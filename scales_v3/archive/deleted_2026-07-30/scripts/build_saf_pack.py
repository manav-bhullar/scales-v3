"""Build Wave 5 real-data pack from SAF (ASAG2024) — TCP congestion control.

Source: Meyerger/ASAG2024 (Hugging Face), data_source == "SAF".
Question: TCP Slow Start vs Congestion Avoidance (cwnd / ss_thresh), 65 answers.

Unlike Mohler (holistic 0–10, often generous), SAF grades are already fraction
credits against a long reference (0.25 / 0.375 / 0.5 / … / 1.0), so gold aligns
better with atomic reference-based marking.

Usage (from scales_v3/):
  .venv/bin/python scripts/build_saf_pack.py           # stratified n=20 smoke
  .venv/bin/python scripts/build_saf_pack.py --full    # all 65 answers
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pyarrow.parquet as pq

PROJECT = Path(__file__).resolve().parents[1]
OUT = PROJECT / "data" / "e2e_eval" / "wave5_real" / "saf_tcp_congestion"
CACHE_CANDIDATES = [
    Path.home()
    / ".cache/huggingface/hub/datasets--Meyerger--ASAG2024"
    / "snapshots/9a7a179de4e227f5e78625bc9ded2d8761f1ff09/train.parquet",
    Path(r"C:\Users\manav\.cache\huggingface\hub\datasets--Meyerger--ASAG2024")
    / r"snapshots\9a7a179de4e227f5e78625bc9ded2d8761f1ff09\train.parquet",
]
LOCAL_SLICE = PROJECT / "data" / "e2e_eval" / "wave5_real" / "saf_tcp_congestion_source.parquet"

# Long-reference variant (fit=10 in _saf_candidates.json)
QUESTION = (
    "In the lecture you have learned about congestion control with TCP. "
    "Name the 2 phases of congestion control and explain how the Congestion "
    "Window (cwnd) and the Slow Start Threshold (ss_thresh) change in each "
    "phase (after initialization, where cwnd = 1 and ss_thresh = advertised "
    "window size) in 1-4 sentences ."
)

TOTAL_MARKS = 5
EXAM_ID = "e2e_wave5_saf_tcp_congestion"

# Concepts must be answerable from the stem (Mohler lesson: no unearnable C1/C4).
RUBRIC = """Total 5 marks:
1) Names both phases: Slow Start and Congestion Avoidance. (1 mark)
2) Slow Start behaviour: while cwnd < ss_thresh, cwnd grows fast
   (typically +1 per ACK → exponential / doubles each RTT) until ss_thresh
   (or loss). (1.5 marks)
3) Congestion Avoidance behaviour: when cwnd >= ss_thresh, cwnd grows more
   slowly (typically linear, e.g. +1 per RTT / after window ACKed). (1.5 marks)
4) Loss / congestion reaction (as in the reference): ss_thresh becomes cwnd/2
   (or similar halving) and cwnd is reset (typically to 1) — may be stated for
   either phase. (1 mark)
Partial credit (0.5 of a concept) when the idea is present but incomplete or
imprecise (e.g. names only one phase; says "grows" without fast vs slow).
Award 0 when absent or clearly wrong (e.g. confuses phases, invents unrelated
mechanisms). ss_thresh stays constant during normal growth in each phase until
a loss event — do not require inventing extra rules beyond the reference."""


def band_for(score_5: float) -> str:
    if score_5 >= 3.75:  # normalized >= 0.75
        return "high"
    if score_5 <= 1.0:
        return "low"
    if score_5 < 2.5:
        return "mid_low"
    return "mid"


def find_cache() -> Path:
    if LOCAL_SLICE.exists():
        return LOCAL_SLICE
    for path in CACHE_CANDIDATES:
        if path.exists():
            return path
    raise FileNotFoundError(
        "ASAG2024 train.parquet not found. Download Meyerger/ASAG2024 once, "
        f"or place a question slice at {LOCAL_SLICE}"
    )


def stratified_sample(rows: list[dict], n: int = 20) -> list[dict]:
    """Keep all weak answers; fill remaining slots from mid then high."""
    by_band: dict[str, list[dict]] = {"mid_low": [], "mid": [], "high": [], "low": []}
    for r in rows:
        by_band[band_for(float(r["normalized_grade"]) * TOTAL_MARKS)].append(r)

    for band in by_band:
        by_band[band].sort(key=lambda r: (float(r["normalized_grade"]), str(r["provided_answer"])))

    picked: list[dict] = []
    # Prefer safety/discrimination: all mid_low (+ low if any)
    picked.extend(by_band["low"])
    picked.extend(by_band["mid_low"])

    remaining = max(0, n - len(picked))
    # ~half mid, ~half high from what's left
    n_mid = remaining // 2
    n_high = remaining - n_mid
    picked.extend(by_band["mid"][:n_mid])
    picked.extend(by_band["high"][:n_high])

    # If still short (small cohort), fill from unused
    if len(picked) < n:
        used = {id(x) for x in picked}
        rest = [r for r in rows if id(r) not in used]
        rest.sort(key=lambda r: float(r["normalized_grade"]))
        picked.extend(rest[: n - len(picked)])

    picked.sort(key=lambda r: (-float(r["normalized_grade"]), str(r["provided_answer"])))
    return picked[:n]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--full",
        action="store_true",
        help="Include all matching SAF answers (65) instead of stratified smoke",
    )
    parser.add_argument("--n", type=int, default=20, help="Stratified sample size (default 20)")
    args = parser.parse_args()

    src = find_cache()
    df = pq.read_table(src).to_pandas()
    if "data_source" in df.columns:
        df = df[df["data_source"] == "SAF"]
    g = df[df["question"] == QUESTION].copy()
    if g.empty:
        raise SystemExit(f"No rows for target question in {src}")

    # Cache a reproducible slice next to the pack (small, no HF dependency later)
    g.to_parquet(LOCAL_SLICE, index=False)

    rows = g.to_dict(orient="records")
    rows.sort(key=lambda r: (-float(r["normalized_grade"]), str(r["provided_answer"])))
    if not args.full:
        rows = stratified_sample(rows, n=args.n)

    question = str(rows[0]["question"]).strip()
    reference = str(rows[0]["reference_answer"]).strip()

    answers = []
    gold = []
    for i, r in enumerate(rows):
        sid = f"SAF_{i:02d}"
        text = str(r["provided_answer"] or "").replace("\xa0", " ").strip()
        answers.append({"student_id": sid, "answer_text": text})

        norm = float(r["normalized_grade"])
        score_5 = round(norm * TOTAL_MARKS, 4)
        lo = max(0.0, round(score_5 - 0.5, 2))
        hi = min(float(TOTAL_MARKS), round(score_5 + 0.5, 2))
        band = band_for(score_5)
        if band == "low":
            lo, hi = 0.0, 0.5
        gold.append(
            {
                "student_id": sid,
                "expected_band": band,
                "expected_score_range": [lo, hi],
                "watch": (
                    f"SAF human grade={norm} → {score_5}/{TOTAL_MARKS} (ASAG2024 normalized_grade)"
                ),
            }
        )

    exam = {
        "exam": {
            "exam_id": EXAM_ID,
            "subject": "Computer Networks (real student answers — SAF)",
            "questions": [
                {
                    "question_id": "Q1",
                    "question_text": question,
                    "reference_answer": reference,
                    "rubric": RUBRIC,
                    "total_marks": TOTAL_MARKS,
                    "student_answers": answers,
                }
            ],
        },
        "meta": {
            "wave": 5,
            "question_key": "Q-REAL2",
            "n_students": len(answers),
            "source": (
                "SAF subset of ASAG2024 (Meyerger/ASAG2024 on Hugging Face). "
                "Real networking-course short answers with fractional human grades "
                "against a long reference — chosen after Mohler gold proved too "
                "lenient/holistic for atomic SCALES marking."
            ),
            "focus": [
                "Real answers with reference-aligned fractional gold (not Mohler holistic)",
                "Stem asks for phases + cwnd/ss_thresh behaviour — all rubric concepts earnable",
                "TCP domain overlap with Wave3 regression without synthetic circularity",
            ],
            "note": "Do not live-grade until VALIDATION.md approved",
            "sample": "full" if args.full else f"stratified_n={len(answers)}",
        },
    }

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "exam.json").write_text(json.dumps(exam, indent=2, ensure_ascii=False), encoding="utf-8")
    (OUT / "gold_labels.json").write_text(
        json.dumps(
            {
                "exam_id": EXAM_ID,
                "question_id": "Q1",
                "question_key": "Q-REAL2",
                "total_marks": TOTAL_MARKS,
                "gold_source": "SAF human grades in ASAG2024 (normalized 0–1 → 0–5)",
                "gold_labels": gold,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    bands: dict[str, int] = {}
    for g_row in gold:
        bands[g_row["expected_band"]] = bands.get(g_row["expected_band"], 0) + 1
    print(f"Wrote {OUT}/exam.json ({len(answers)} answers) and gold_labels.json")
    print("bands:", bands)
    print(f"source slice cached at {LOCAL_SLICE}")


if __name__ == "__main__":
    main()
