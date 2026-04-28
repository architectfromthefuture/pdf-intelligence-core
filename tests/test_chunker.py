from pdf_core.index.chunker import chunk_markdown_file


def test_chunker_windows_and_ids(tmp_path):
    md = tmp_path / "doc.md"
    body = "ABCDEFGHIJ" * 200
    md.write_text(body, encoding="utf-8")

    payload = chunk_markdown_file(md, max_chars=50, overlap=10)
    assert payload["stem"] == "doc"
    assert len(payload["chunks"]) >= 2
    ids = [c["id"] for c in payload["chunks"]]
    assert all(x.startswith("doc:") for x in ids)
    assert ids == sorted(ids)
