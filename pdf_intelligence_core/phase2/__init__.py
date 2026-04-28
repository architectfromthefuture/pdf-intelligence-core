"""Phase 2 — chunking, embeddings, vector index, retrieval."""

from pdf_intelligence_core.phase2.chunk import chunk_markdown
from pdf_intelligence_core.phase2.embed import Embedder
from pdf_intelligence_core.phase2.index import MemoryVectorIndex
from pdf_intelligence_core.phase2.retrieve import retrieve

__all__ = [
    "Embedder",
    "MemoryVectorIndex",
    "chunk_markdown",
    "retrieve",
]
