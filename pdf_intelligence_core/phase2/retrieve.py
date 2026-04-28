"""Top-k retrieval over the index."""

from __future__ import annotations

from pdf_intelligence_core.phase2.embed import Embedder
from pdf_intelligence_core.phase2.index import MemoryVectorIndex
from pdf_intelligence_core.types import IndexRecord


def retrieve(
    index: MemoryVectorIndex,
    embedder: Embedder,
    query: str,
    *,
    top_k: int = 5,
) -> list[tuple[float, IndexRecord]]:
    qvec = embedder.encode([query])[0]
    return index.search(qvec, top_k=top_k)
