"""Prove the evidence-verification fix on the two real false-DEFER cases."""

from __future__ import annotations

import json
from pathlib import Path

from scales.services.text_utils import token_containment, verify_evidence

ROOT = Path("data/exams/e2e_wave2_tcp_handshake_groq")


def main() -> None:
    g = json.loads((ROOT / "grading_results.json").read_text(encoding="utf-8"))
    answers = {
        a["student_id"]: a["answer_text"]
        for a in json.loads((ROOT / "student_answers.json").read_text(encoding="utf-8"))[
            "student_answers"
        ]
    }
    cgr = {(r["student_id"], r["concept_id"]): r for r in g["cgr_results"]}

    checks = [
        ("STU_GOOD", "Q1_C3", "curly apostrophe"),
        ("STU_GOOD_ALT", "Q1_C4", "arrow + list-marker reformat"),
        # Control: a genuine unrelated fabrication must still fail.
        ("__control__", "__none__", "disjoint vocabulary (should be False)"),
    ]

    out = []
    for sid, cid, note in checks:
        if sid == "__control__":
            ev, ans = "UDP datagram checksum retransmission", answers["STU_GOOD"]
        else:
            ev = cgr[(sid, cid)]["evidence_span"]
            ans = answers[sid]
        ok = verify_evidence(ev, ans)
        cont = token_containment(ev, ans)
        out.append(f"{sid}/{cid} [{note}]: verify_evidence={ok} token_containment={cont:.3f}")

    Path("data/e2e_eval/wave2/FIX_VERIFICATION.txt").write_text(
        "\n".join(out) + "\n", encoding="utf-8"
    )
    print("\n".join(out).encode("ascii", "replace").decode())


if __name__ == "__main__":
    main()
