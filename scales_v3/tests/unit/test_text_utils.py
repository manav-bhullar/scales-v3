"""Unit tests for text_utils."""

import pytest

from scales.services.text_utils import (
    fuzzy_keyword_match,
    normalize_text,
    token_containment,
    verify_evidence,
)


def test_exact_substring_match():
    assert verify_evidence("TCP uses", "TCP uses handshake") is True


def test_normalized_match_extra_whitespace():
    assert verify_evidence("TCP  uses", "TCP uses handshake") is True


def test_normalized_match_newlines():
    assert verify_evidence("TCP\nuses", "TCP uses handshake") is True


def test_normalized_match_case():
    assert verify_evidence("tcp USES", "TCP uses handshake") is True


def test_no_match_hallucinated():
    assert verify_evidence("UDP protocol", "TCP uses handshake") is False


def test_empty_evidence_vacuous_true():
    assert verify_evidence("", "anything") is True


def test_normalize_text_collapses_whitespace():
    assert normalize_text("  A \n B  ") == "a b"


# ─── Unicode punctuation drift (bugfix: false "hallucinated quote" DEFER) ───


def test_curly_apostrophe_folds_to_straight():
    # LLM re-quotes with a curly apostrophe; student wrote a straight one.
    assert normalize_text("server\u2019s SYN") == "server's syn"


def test_verify_evidence_curly_apostrophe_match():
    # Real STU_GOOD/C3 case: only difference is ' (U+2019) vs '.
    evidence = "confirm the server\u2019s SYN."
    answer = "Finally the client sends an ACK to confirm the server's SYN."
    assert verify_evidence(evidence, answer) is True


def test_verify_evidence_arrow_and_dash_folded():
    evidence = "client \u2192 server \u2014 SYN"
    answer = "the flow is client -> server - SYN segment"
    assert verify_evidence(evidence, answer) is True


# ─── Reformatting / paraphrase fallback ───


def test_verify_evidence_reformatted_list_markers():
    # Real STU_GOOD_ALT/C4 case: evidence concatenates the student's own
    # numbered lines; every word is present but not as a contiguous substring.
    evidence = (
        "Client server: SYN with starting sequence number to request a connection. "
        "Server client: SYN-ACK carrying the server ISN. "
        "Client server: ACK confirming the server SYN."
    )
    answer = (
        "Connection setup uses three steps.\n"
        "1) Client server: SYN with starting sequence number to request a connection.\n"
        "2) Server client: SYN-ACK carrying the server ISN.\n"
        "3) Client server: ACK confirming the server SYN."
    )
    assert verify_evidence(evidence, answer) is True


def test_verify_evidence_true_hallucination_still_rejected():
    # Disjoint vocabulary must still fail even with the fuzzy fallback.
    assert verify_evidence("UDP datagram checksum", "TCP uses a three-way handshake") is False


def test_token_containment_scores():
    assert token_containment("SYN ACK", "client sends SYN then ACK") == 1.0
    assert token_containment("UDP checksum", "TCP handshake only") == 0.0


def test_keyword_search_case_insensitive():
    score, found = fuzzy_keyword_match(["syn"], "Client sends SYN packet")
    assert score == 1.0
    assert found == ["syn"]


def test_keyword_partial_word_not_found():
    score, found = fuzzy_keyword_match(["hand"], "handshake process")
    assert score == 0.0
    assert found == []


def test_keyword_variant_phrase():
    score, found = fuzzy_keyword_match(
        ["SYN-ACK"],
        "3-step setup process for connection",
        acceptable_variants=["3-step setup"],
    )
    assert score > 0.0
    assert found == []


def test_empty_keywords_score_one():
    score, found = fuzzy_keyword_match([], "anything")
    assert score == 1.0
    assert found == []


# ─── TC-007: paraphrase-tolerant variant matching ────────────────────────────


def test_variant_paraphrase_token_containment_hits():
    # Exact OS1 false-DEFER case (MID_01/Q1_C1): variant "threads run inside a
    # process" vs answer wording "threads are smaller units inside it" — 3/4
    # content tokens present, no exact substring.
    score, found = fuzzy_keyword_match(
        ["independent", "execution unit", "within a process"],
        "A process is a running program and threads are smaller units inside it.",
        acceptable_variants=["threads run inside a process"],
    )
    assert found == []
    assert score == pytest.approx(1.0 / 3.0)


def test_variant_disjoint_vocabulary_does_not_hit():
    score, found = fuzzy_keyword_match(
        ["isolation", "corruption", "synchronization", "races"],
        "But threads can interfere with each other.",
        acceptable_variants=["shared memory bugs", "need for locks"],
    )
    assert score == 0.0
    assert found == []


def test_variant_stopword_only_does_not_hit():
    score, found = fuzzy_keyword_match(
        ["checksum"],
        "totally unrelated text",
        acceptable_variants=["of the and"],
    )
    assert score == 0.0
    assert found == []
