# Pipeline reference

This document aligns the **story** with **modules** and **data shapes**.

## End-to-end flow

1. **Validated** — `phase1.validate.validate_pdf` checks magic bytes and `pypdf` parseability.
2. **Extracted** — `phase1.extract.extract_text` returns one string per page (may be empty).
3. **Normalized Markdown** — `phase1.normalize.normalize_to_markdown` emits stable `## Page N` sections.
4. **Audited** — `phase1.audit.audit_normalized` records warnings (e.g. empty pages, very short output).
5. **Chunked** — `phase2.chunk.chunk_markdown` yields `Chunk` records (sliding windows per page).
6. **Embedded** — `phase2.embed.HashEmbedder` (default) or any `Embedder` implementation.
7. **Indexed** — `phase2.index.MemoryVectorIndex` stores `IndexRecord` rows (chunk id + vector).
8. **Retrieved** — `phase2.retrieve.retrieve` runs cosine search for a query string.
9. **Graph projection** — `phase3.graph.project_document_graph` builds `DocumentGraph` with:
   - **NEXT_CHUNK** edges in chunk order
   - **SIMILAR** edges when cosine similarity exceeds a threshold (small-doc friendly)

## Orchestration

`pdf_intelligence_core.pipeline.run_pipeline` wires the stages in order and returns a `PipelineResult`.

## Extension points

| Replace | When |
|--------|------|
| Extract | Need OCR, layout blocks, or tables |
| `Embedder` | Need semantic vectors (e.g. sentence-transformers, APIs) |
| `MemoryVectorIndex` | Need persistence, ANN, or hybrid sparse+dense |
| Graph builder | Need entity/relation extraction, citation graphs, or section trees |

## Versioning

Pipeline JSON or artifact schemas are not stable before `1.0.0`; pin commits for reproducibility.
