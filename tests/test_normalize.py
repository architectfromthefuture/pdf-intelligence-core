"""Tests for ingest normalize()."""

from pdf_core.ingest.normalize import normalize


def test_hyphen_line_breaks_removed():
    assert normalize("exam-\nple") == "example"


def test_repeated_blank_lines_collapse():
    out = normalize("line one\n\n\n\nline two")
    assert "\n\n\n" not in out
    # Blank-only lines are dropped; paragraphs collapse to single newlines between text lines.
    assert out == "line one\nline two"


def test_duplicate_lines_removed():
    out = normalize("alpha\nbeta\nalpha")
    lines = [ln for ln in out.split("\n") if ln.strip()]
    assert lines == ["alpha", "beta"]
