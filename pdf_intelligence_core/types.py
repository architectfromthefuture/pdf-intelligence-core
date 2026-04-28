"""Shared datatypes for pipeline artifacts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

EdgeKind = Literal["NEXT_CHUNK", "SIMILAR"]


@dataclass(frozen=True)
class ArtifactRef:
    """Opaque handle for intermediate blobs (paths, hashes, or URIs)."""

    kind: Literal["pdf_bytes", "markdown", "chunks_json"]
    ref: str
    meta: dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditReport:
    """Structural / quality findings after normalization."""

    warnings: list[str]
    pages_with_text: int
    pages_total: int
    char_count: int


@dataclass
class Chunk:
    """One retrieval unit."""

    id: str
    text: str
    page_start: int
    page_end: int
    token_estimate: int


@dataclass
class IndexRecord:
    """Chunk plus embedding stored for retrieval."""

    chunk_id: str
    text: str
    embedding: list[float]
    page_start: int
    page_end: int


@dataclass
class GraphNode:
    id: str
    chunk_id: str
    summary: str
    page_start: int
    page_end: int


@dataclass
class GraphEdge:
    source: str
    target: str
    kind: EdgeKind
    weight: float


@dataclass
class DocumentGraph:
    """Projected structure over chunks (minimal property graph slice)."""

    nodes: list[GraphNode]
    edges: list[GraphEdge]

