import json

from pdf_core.graph.extractor import nodes_from_chunk_file
from pdf_core.graph.schema import NodeRecord


def test_extractor_orders_by_ord(tmp_path):
    p = tmp_path / "sample.json"
    p.write_text(
        json.dumps(
            {
                "stem": "z",
                "source_path": str(p),
                "chunks": [
                    {"id": "z:00001", "text": "b", "ord": 1, "source_md": "z.md"},
                    {"id": "z:00000", "text": "a", "ord": 0, "source_md": "z.md"},
                ],
            }
        ),
        encoding="utf-8",
    )
    nodes = nodes_from_chunk_file(p)
    ords = [n.ord for n in nodes]
    assert ords == sorted(ords)
    assert isinstance(nodes[0], NodeRecord)
