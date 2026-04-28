"""Tests for pdf-intelligence-core."""

from io import BytesIO

from pypdf import PdfWriter

from pdf_intelligence_core.phase1.normalize import normalize_to_markdown
from pdf_intelligence_core.phase1.validate import PDF_MAGIC
from pdf_intelligence_core.phase1.validate import validate_pdf
from pdf_intelligence_core.phase2.chunk import chunk_markdown
from pdf_intelligence_core.phase2.embed import HashEmbedder
from pdf_intelligence_core.phase3.graph import project_document_graph
from pdf_intelligence_core.pipeline import run_pipeline


def tiny_blank_pdf() -> bytes:
    w = PdfWriter()
    w.add_blank_page(width=612, height=792)
    buf = BytesIO()
    w.write(buf)
    return buf.getvalue()


def test_validate_accepts_generated_pdf():
    data = tiny_blank_pdf()
    assert data.startswith(PDF_MAGIC)
    ok, msg = validate_pdf(data)
    assert ok
    assert msg == "ok"


def test_normalize_and_chunk_multiple_pages_without_headers():
    pages = ["First page body.", "Second page line one.\nSecond line."]
    md = normalize_to_markdown(pages)
    chunks = chunk_markdown(md)
    texts = "\n".join(c.text for c in chunks).lower()
    assert "first page body" in texts
    assert "second page line" in texts


def test_pipeline_runs_through_graph():
    pdf = tiny_blank_pdf()
    res = run_pipeline(pdf)
    assert res.validation_message == "ok"
    assert res.audit.pages_total >= 1
    assert isinstance(res.markdown, str)
    assert len(res.graph.nodes) == len(res.chunks)


def test_hash_embedder_deterministic():
    e = HashEmbedder()
    a = e.encode(["hello"])
    b = e.encode(["hello"])
    assert a == b
    assert len(a[0]) == e.dim


def test_graph_projection_edges():
    from pdf_intelligence_core.types import Chunk, IndexRecord

    chunks = [
        Chunk(id="c1", text="aaa", page_start=1, page_end=1, token_estimate=10),
        Chunk(id="c2", text="bbb", page_start=1, page_end=1, token_estimate=10),
    ]
    emb = HashEmbedder()
    vecs = emb.encode([c.text for c in chunks])
    recs = [
        IndexRecord(
            chunk_id=chunks[i].id,
            text=chunks[i].text,
            embedding=vecs[i],
            page_start=1,
            page_end=1,
        )
        for i in range(2)
    ]
    g = project_document_graph(chunks, recs, similarity_edge_threshold=-1.0, top_similar_per_node=1)
    next_edges = [e for e in g.edges if e.kind == "NEXT_CHUNK"]
    assert len(next_edges) == 1
