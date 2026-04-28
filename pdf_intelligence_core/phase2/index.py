"""In-memory vector index (cosine similarity on L2-normalized vectors)."""

from __future__ import annotations

from pdf_intelligence_core.types import IndexRecord


class MemoryVectorIndex:
    """Minimal ANN substitute: brute-force cosine similarity."""

    def __init__(self) -> None:
        self._rows: list[IndexRecord] = []

    def upsert_many(self, records: list[IndexRecord]) -> None:
        self._rows.extend(records)

    def search(self, query_vec: list[float], *, top_k: int = 8) -> list[tuple[float, IndexRecord]]:
        def dot(a: list[float], b: list[float]) -> float:
            return sum(x * y for x, y in zip(a, b, strict=False))

        qn = dot(query_vec, query_vec) ** 0.5 or 1.0
        q = [x / qn for x in query_vec]

        scored: list[tuple[float, IndexRecord]] = []
        for r in self._rows:
            dn = dot(r.embedding, r.embedding) ** 0.5 or 1.0
            cand = [x / dn for x in r.embedding]
            sim = dot(q, cand)
            scored.append((sim, r))
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[:top_k]
