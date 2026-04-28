# Phase 2 — Indexing / memory

Phase 2 consumes Markdown from `data/markdown/`, writes **chunk JSON**, **deterministic embeddings**, a **FAISS** index on disk, retriever hooks, and **trace** JSON for observability.

## Steps

1. **Chunk** — Sliding character windows per file (`configs/settings.yaml`: `chunk.max_chars`, `chunk.overlap_chars`). Each chunk gets a stable id `{stem}:{index:05d}`.
2. **Embed** — Deterministic hash-derived vectors (normalized for cosine-style inner product search). No external API calls.
3. **Vector store** — `faiss.IndexFlatIP` on L2-normalized vectors; sidecar `meta.json` maps row order to chunk ids/previews.
4. **Artifacts** — `data/chunks/*.json`, `data/embeddings/matrix.npy`, `data/vectors/index.faiss`, `data/vectors/meta.json`, `data/traces/index_last.json`.

## CLI

`pdf-index` rebuilds the corpus index from all `*.md` inputs.

`pdf-query` embeds a query string with the **same** deterministic embedder and reads `data/vectors/` for top-k rows.

## Operational notes

Replace the embedder with a real model when semantic quality matters; until then, retrieval remains **reproducible plumbing**, not benchmarks.
