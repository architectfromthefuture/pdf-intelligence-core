"""Create structural edges from sorted chunk order (per document)."""

from __future__ import annotations

from pdf_core.graph.schema import EdgeRecord, NodeRecord


def build_next_chunk_edges(nodes: list[NodeRecord]) -> list[EdgeRecord]:
    """Connect consecutive chunks within the same ``doc_stem`` (``ord`` ascending)."""
    by_doc: dict[str, list[NodeRecord]] = {}
    for n in nodes:
        by_doc.setdefault(n.doc_stem, []).append(n)
    edges: list[EdgeRecord] = []
    eid = 0
    for doc, row in by_doc.items():
        row = sorted(row, key=lambda n: n.ord)
        for a, b in zip(row, row[1:], strict=False):
            eid += 1
            edges.append(
                EdgeRecord(
                    id=f"e_{doc}_{eid:05d}",
                    source=a.id,
                    target=b.id,
                    kind="NEXT_CHUNK",
                    weight=1.0,
                )
            )
    return edges
