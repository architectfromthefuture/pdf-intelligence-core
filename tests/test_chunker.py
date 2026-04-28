"""Tests for index chunk_text()."""

from pdf_core.index.chunker import chunk_text


def test_chunk_count_chunk_size_and_ids():
    text = " ".join(str(i) for i in range(1000))

    got = chunk_text(text, chunk_size=500)

    assert got["total_chunks"] == 2
    assert got["chunk_size"] == 500
    assert got["chunks"][0]["chunk_id"] == "chunk_0000"
    assert got["chunks"][1]["chunk_id"] == "chunk_0001"
    assert len(got["chunks"][0]["text"].split()) == 500
    assert len(got["chunks"][1]["text"].split()) == 500


def test_empty_text_yields_zero_chunks():
    assert chunk_text("")["total_chunks"] == 0
