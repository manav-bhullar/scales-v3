"""Inspect DEFER signal values for Wave 2 (analysis only). Writes UTF-8 report."""

from __future__ import annotations

import json
from pathlib import Path

from scales.services.text_utils import fuzzy_keyword_match, normalize_text, verify_evidence

ROOT = Path("data/exams/e2e_wave2_tcp_handshake_groq")
OUT = Path("data/e2e_eval/wave2/DEFER_DIAGNOSIS.txt")


def char_diff_note(evidence: str, answer: str) -> str:
    """Explain why normalized substring match fails, if it does."""
    ev_n = normalize_text(evidence)
    ans_n = normalize_text(answer)
    if not ev_n:
        return "evidence empty"
    if ev_n in ans_n:
        return "MATCHES after normalize"
    # Find non-ascii chars in evidence
    non_ascii = sorted({(c, hex(ord(c))) for c in evidence if ord(c) > 127})
    # ASCII-fold both and retry
    def fold(s: str) -> str:
        return (
            s.replace("\u2019", "'")
            .replace("\u2018", "'")
            .replace("\u201c", '"')
            .replace("\u201d", '"')
            .replace("\u2192", "->")
            .replace("\u2013", "-")
            .replace("\u2014", "-")
        )
    folded_ok = fold(ev_n) in fold(ans_n)
    return (
        f"NO match after normalize; non_ascii_in_evidence={non_ascii}; "
        f"match_after_punct_fold={folded_ok}"
    )


def main() -> None:
    g = json.loads((ROOT / "grading_results.json").read_text(encoding="utf-8"))
    cqas = json.loads((ROOT / "cqa_tuples.json").read_text(encoding="utf-8"))["cqa_tuples"]
    answers = {
        a["student_id"]: a["answer_text"]
        for a in json.loads((ROOT / "student_answers.json").read_text(encoding="utf-8"))[
            "student_answers"
        ]
    }
    cqa_map = {c["concept_id"]: c for c in cqas}
    cgr = {(r["student_id"], r["concept_id"]): r for r in g["cgr_results"]}

    lines: list[str] = ["=== DEFER cases (Wave 2) ==="]
    for t in g["cbte_results"]:
        if t["decision"] != "DEFER":
            continue
        c = cgr[(t["student_id"], t["concept_id"])]
        cqa = cqa_map[t["concept_id"]]
        ev = c["evidence_span"]
        ans = answers[t["student_id"]]
        lines.append(f"\n{t['student_id']}/{t['concept_id']} verdict={c['verdict']} marks={c['marks_awarded']}")
        lines.append(f"  tier={t['tier_resolved']} trust={t['trust_score']:.3f}")
        lines.append(f"  sig1_evidence_verified={t['signal_1_evidence_verified']}")
        lines.append(f"  sig2_nli={t['signal_2_nli_score']}  sig4_keyword={t['signal_4_keyword_score']}")
        lines.append(f"  reason={t['reason']}")
        lines.append(f"  evidence_span={ev!r}")
        lines.append(f"  diag={char_diff_note(ev, ans)}")

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
