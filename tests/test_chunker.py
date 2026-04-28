from pdf_core.index.chunker import chunk_text


def test_word_window_chunk_ids_and_counts():
    words = [str(i) for i in range(1000)]
    text = " ".join(words)

    got = chunk_text(text, chunk_size=500)

    assert got["strategy"] == "fixed_word_window"
    assert got["chunk_size"] == 500
    assert got["total_chunks"] == 2
    assert got["chunks"][0]["chunk_id"] == "chunk_0000"
    assert got["chunks"][1]["chunk_id"] == "chunk_0001"
    assert got["chunks"][0]["start_word"] == 0
    assert got["chunks"][1]["start_word"] == 500


def test_empty_document():
    assert chunk_text("")["total_chunks"] == 0
