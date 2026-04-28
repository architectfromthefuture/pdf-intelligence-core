import json

from pdf_core.graph.extractor import nodes_from_chunk_file
from pdf_core.graph.schema import NodeRecord


def test_extractor_word_windows_and_orders(tmp_path):
    p = tmp_path / "sample.json"
    p.write_text(
        json.dumps(
            {
                "doc_id": "z",
                "chunks": [
                    {
                        "chunk_id": "chunk_0001",
                        "text": "later",
                        "start_word": 10,
                        "end_word": 11,
                    },
                    {
                        "chunk_id": "chunk_0000",
                        "text": "first",
                        "start_word": 0,
                        "end_word": 10,
                    },
                ],
                "strategy": "fixed_word_window",
                "chunk_size": 500,
                "total_chunks": 2,
            }
        ),
        encoding="utf-8",
    )
    nodes = nodes_from_chunk_file(p)
    assert [n.ord for n in nodes] == [0, 1]
    assert nodes[0].id == "z__chunk_0000"
    assert isinstance(nodes[0], NodeRecord)
