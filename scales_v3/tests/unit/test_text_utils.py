"""Unit tests for text_utils."""

from scales.services.text_utils import fuzzy_keyword_match, normalize_text, verify_evidence


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
