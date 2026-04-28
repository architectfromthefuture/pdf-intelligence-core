# pdf-intelligence-core

A **small, observable, file-backed** pipeline: PDFs in `data/inbox/` become normalized Markdown, audited JSON, chunked JSON, a local **FAISS** index with trace files, and a **deterministic chunk graph** exported as JSON. Everything is inspectable on disk—no hosted database, Docker, web UI, or LLM inference in the default path.

## Phases at a glance

| Phase | Responsibility | Inspect |
|-------|-----------------|--------|
| **1 — Ingestion** | Validate (PyMuPDF), extract (`pymupdf4llm` → fallback `pdfplumber`), normalize, audits | `data/markdown/*.md`, `data/audit/*.json` |
| **2 — Index / memory** | Chunk Markdown, deterministic embeddings (no API), **FAISS**, traces | `data/chunks/*.json`, `data/embeddings/matrix.npy`, `data/vectors/`, `data/traces/` |
| **3 — Graph** | Structural edges from chunk order only | `data/graphs/nodes.json`, `data/graphs/edges.json`, `data/graphs/traces/` |

See `docs/architecture.md` and `docs/phase_*.md` for detail.

## Flow

```txt
PDF
→ validated → extracted → normalized Markdown → audited
→ chunked → embedded → FAISS index → retrievable
→ deterministic graph projection (chunks only)
```

## Quickstart

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"   # or: pip install -r requirements.txt
```

1. Drop one or more PDFs into `data/inbox/`.
2. `pdf-ingest` — writes Markdown + audit JSON under `configs/settings.yaml` paths.
3. `pdf-index` — builds chunk JSON, `embeddings/matrix.npy`, `vectors/index.faiss` + `meta.json`, trace.
4. `pdf-graph` — builds `nodes.json` / `edges.json`.
5. `pdf-query "your question"` — runs against the **local FAISS** index using the deterministic embedder.

## Honest limits

- **No OCR guarantee** beyond what extractors recover; scanned pages may yield little text.
- **Embeddings are hashed vectors** by default—they are deterministic and reproducible, not semantic SOTA (swap `embeddings/` generation when you introduce a model).
- **Index is brute-force-flat** (`IndexFlatIP`) with unit-normal vectors for cosine-style search—fine for demos; swap for IVF/HNSW when scale grows.

## Development

```bash
pytest
ruff check .
```

## License

MIT — see `LICENSE`.
