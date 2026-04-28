"""End-to-end orchestration."""

from __future__ import annotations

from dataclasses import dataclass, field

from pdf_intelligence_core.phase1.audit import audit_normalized
from pdf_intelligence_core.phase1.extract import extract_text
from pdf_intelligence_core.phase1.normalize import normalize_to_markdown
from pdf_intelligence_core.phase1.validate import validate_pdf
from pdf_intelligence_core.phase2.chunk import chunk_markdown
from pdf_intelligence_core.phase2.embed import Embedder, HashEmbedder
from pdf_intelligence_core.phase2.index import MemoryVectorIndex
from pdf_intelligence_core.phase2.retrieve import retrieve
from pdf_intelligence_core.phase3.graph import project_document_graph
from pdf_intelligence_core.types import (
    AuditReport,
    Chunk,
    DocumentGraph,
    IndexRecord,
)


@dataclass
class PipelineConfig:
    chunk_max_chars: int = 1200
    chunk_overlap_chars: int = 100
    retrieve_top_k: int = 5
    similarity_edge_threshold: float = 0.35
    top_similar_edges: int = 2


@dataclass
class PipelineResult:
    validation_message: str
    markdown: str
    audit: AuditReport
    chunks: list[Chunk]
    index_records: list[IndexRecord]
    graph: DocumentGraph
    retrieval_sample: list[tuple[float, IndexRecord]] = field(default_factory=list)


def run_pipeline(
    pdf_bytes: bytes,
    *,
    embedder: Embedder | None = None,
    query: str = "summarize main topics",
    config: PipelineConfig | None = None,
) -> PipelineResult:
    """
    Runs all phases in order:

    validate → extract → normalize → audit → chunk → embed → index → retrieve → graph.
    """
    cfg = config or PipelineConfig()
    emb = embedder or HashEmbedder()

    ok, msg = validate_pdf(pdf_bytes)
    if not ok:
        return PipelineResult(
            validation_message=msg,
            markdown="",
            audit=AuditReport(warnings=[], pages_with_text=0, pages_total=0, char_count=0),
            chunks=[],
            index_records=[],
            graph=DocumentGraph(nodes=[], edges=[]),
            retrieval_sample=[],
        )

    page_texts = extract_text(pdf_bytes)
    md = normalize_to_markdown(page_texts)
    audit = audit_normalized(page_texts, md)

    chunks = chunk_markdown(
        md,
        max_chars=cfg.chunk_max_chars,
        overlap_chars=cfg.chunk_overlap_chars,
    )

    vectors = emb.encode([c.text for c in chunks])
    records = [
        IndexRecord(
            chunk_id=c.id,
            text=c.text,
            embedding=vectors[i],
            page_start=c.page_start,
            page_end=c.page_end,
        )
        for i, c in enumerate(chunks)
    ]

    idx = MemoryVectorIndex()
    idx.upsert_many(records)
    retrieval_sample = retrieve(idx, emb, query, top_k=cfg.retrieve_top_k)

    graph = project_document_graph(
        chunks,
        records,
        similarity_edge_threshold=cfg.similarity_edge_threshold,
        top_similar_per_node=cfg.top_similar_edges,
    )

    return PipelineResult(
        validation_message=msg,
        markdown=md,
        audit=audit,
        chunks=chunks,
        index_records=records,
        graph=graph,
        retrieval_sample=retrieval_sample,
    )
