"""Inspect SAF grade granularity: raw `grade` vs `normalized_grade`."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import pyarrow.parquet as pq

CACHE = Path(
    r"C:\Users\manav\.cache\huggingface\hub\datasets--Meyerger--ASAG2024"
    r"\snapshots\9a7a179de4e227f5e78625bc9ded2d8761f1ff09\train.parquet"
)

df = pq.read_table(CACHE).to_pandas()
saf = df[df["data_source"] == "SAF"].copy()

print("SAF rows:", len(saf))
print()
print("--- raw `grade` distinct values ---")
raw = Counter(round(float(g), 4) for g in saf["grade"])
for v, c in sorted(raw.items()):
    print(f"  {v:>6} : {c}")

print()
print("--- normalized_grade distinct values ---")
norm = Counter(round(float(g), 4) for g in saf["normalized_grade"])
for v, c in sorted(norm.items()):
    print(f"  {v:>6} : {c}")

print()
print("distinct raw grades:", len(raw), "| distinct normalized:", len(norm))

# The TCP congestion question specifically
target = [q for q in saf["question"].unique() if "congestion control with TCP" in q]
for q in target:
    g = saf[saf["question"] == q]
    print()
    print("=== TCP question, n =", len(g))
    print("raw grade values:", sorted(Counter(round(float(x), 3) for x in g["grade"]).items()))
    print("max raw grade:", g["grade"].max())

# Compare with Mohler granularity for reference
moh = df[df["data_source"] == "Mohler"]
print()
print("--- Mohler raw grade distinct (for comparison) ---")
print(sorted(Counter(round(float(x), 3) for x in moh["grade"]).items()))
