"""Build a minimal DocumentGraph over chunks."""

from __future__ import annotations

import math

from pdf_intelligence_core.types import Chunk, DocumentGraph, GraphEdge, GraphNode, IndexRecord


def _snippet(text: str, n: int = 120) -> str:
    t = text.replace("\n", " ").strip()
    return t[:n] + ("..." if len(t) > n else "")


def project_document_graph(
    chunks: list[Chunk],
    records: list[IndexRecord],
    *,
    similarity_edge_threshold: float = 0.35,
    top_similar_per_node: int = 2,
) -> DocumentGraph:
    """
    Nodes mirror chunks (with short summaries). Edges:

    - NEXT_CHUNK: sequential reading order within the chunked list.

    - SIMILAR: pairs whose cosine similarity exceeds ``similarity_edge_threshold``.
      Comparisons use stored embeddings only (cheap for small docs).
    """
    nodes: list[GraphNode] = []
    for ch in chunks:
        nodes.append(
            GraphNode(
                id=f"n_{ch.id}",
                chunk_id=ch.id,
                summary=_snippet(ch.text),
                page_start=ch.page_start,
                page_end=ch.page_end,
            )
        )

    edges: list[GraphEdge] = []

    node_ids = [n.id for n in nodes]
    for i in range(len(node_ids) - 1):
        edges.append(GraphEdge(source=node_ids[i], target=node_ids[i + 1], kind="NEXT_CHUNK", weight=1.0))

    def cosine(a: list[float], b: list[float]) -> float:
        if len(a) != len(b) or not a:
            return 0.0
        dp = sum(x * y for x, y in zip(a, b, strict=False))
        na = math.sqrt(sum(x * x for x in a))
        nb = math.sqrt(sum(y * y for y in b))
        if na == 0 or nb == 0:
            return 0.0
        return dp / (na * nb)

    for i, ai in enumerate(records):
        sims: list[tuple[float, int]] = []
        for j, aj in enumerate(records):
            if i == j:
                continue
            sims.append((cosine(ai.embedding, aj.embedding), j))
        sims.sort(key=lambda x: x[0], reverse=True)
        for sim, j in sims[:top_similar_per_node]:
            if sim < similarity_edge_threshold:
                continue
            src, tgt = records[i].chunk_id, records[j].chunk_id
            src_n, tgt_n = f"n_{src}", f"n_{tgt}"
            edges.append(GraphEdge(source=src_n, target=tgt_n, kind="SIMILAR", weight=float(sim)))

    return DocumentGraph(nodes=nodes, edges=edges)
