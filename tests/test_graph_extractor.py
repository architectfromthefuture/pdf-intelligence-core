"""Tests for graph extract_entities()."""

from pdf_core.graph.extractor import extract_entities


def test_extracts_capitalized_multi_word_phrases():
    text = "We read New York Times and later Microsoft Word specs."
    entities = extract_entities(text)["entities"]

    assert "New York Times" in entities
    assert "Microsoft Word" in entities


def test_result_includes_method_field():
    got = extract_entities("Any Text Here")

    assert "method" in got
    assert got["method"] == "regex_capital_phrase"
