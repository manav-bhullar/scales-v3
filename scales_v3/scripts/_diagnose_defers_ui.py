"""Diagnose website defer rates."""
from __future__ import annotations

import json
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    try:
        with urllib.request.urlopen("http://127.0.0.1:8000/api/exams", timeout=5) as r:
            exams = json.loads(r.read().decode())
        print("=== API /exams (website dashboard) ===")
        for e in exams:
            print(
                f"{e['exam_id']}: phase={e['phase']} "
                f"defer={e['deferred_count']} rate={e['defer_rate']} "
                f"graded={e['graded_count']}/{e['total_students']} "
                f"review_complete={e['review_complete']}"
            )
    except Exception as ex:  # noqa: BLE001
        print("API down:", ex)

    for exam_id in (
        "e2e_wave1_tcp_handshake",
        "e2e_wave2_tcp_handshake_groq",
        "e2e_wave3_tcp_handshake_expanded",
    ):
        p = ROOT / "data" / "exams" / exam_id / "grading_results.json"
        if not p.exists():
            print(f"\n{exam_id}: no grading_results.json on disk")
            continue
        g = json.loads(p.read_text(encoding="utf-8"))
        cbte = g.get("cbte_results", [])
        cgr = {(r["student_id"], r["concept_id"]): r for r in g.get("cgr_results", [])}
        dec = Counter(r["decision"] for r in cbte)
        print(f"\n=== {exam_id} ===")
        print("decisions", dict(dec), "n=", len(cbte))
        reason_buckets: Counter[str] = Counter()
        for r in cbte:
            if r["decision"] != "DEFER":
                continue
            reason = r.get("reason", "")
            if "hallucinated" in reason.lower():
                bucket = "false_evidence_veto"
            elif reason.startswith("Tier 3"):
                bucket = "tier3_below_tau"
            elif "Tier 1" in reason:
                bucket = "tier1_other"
            else:
                bucket = "other"
            reason_buckets[bucket] += 1
            c = cgr.get((r["student_id"], r["concept_id"]), {})
            print(
                f"  {r['student_id']}/{r['concept_id']} "
                f"verdict={c.get('verdict')} tier={r.get('tier_resolved')} "
                f"trust={r.get('trust_score')} kw={r.get('signal_4_keyword_score')} "
                f"nli={r.get('signal_2_nli_score')} | {reason[:80]}"
            )
        print("defer buckets", dict(reason_buckets))


if __name__ == "__main__":
    main()
