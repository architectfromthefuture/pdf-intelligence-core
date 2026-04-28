from pdf_core.ingest.normalize import normalize


def test_hyphen_newline_joins_words():
    assert normalize("exam-\nple") == "example"


def test_duplicate_nonempty_lines_removed_second_occurrence():
    body = "alpha\nbeta\nalpha\n"
    out = normalize(body)
    lines = [ln for ln in out.split("\n") if ln.strip()]
    assert lines.count("alpha") == 1
