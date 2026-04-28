# pdf-intelligence-core

A **small, observable, file-backed** pipeline: PDFs in `data/inbox/` become normalized Markdown, audited JSON, chunked JSON, sentence embeddings (**SentenceTransformers**), a local **FAISS** index with traces, and a **deterministic chunk graph** exported as JSON. Everything stays on disk for inspection—no hosted database or web UI.

## Phases at a glance

| Phase | Responsibility | Inspect |
|-------|-----------------|--------|
| **1 — Ingestion** | Validate (PyMuPDF), extract (`pymupdf4llm` → fallback `pdfplumber`), normalize, audits | `data/markdown/*.md`, `data/audit/*.json` |
| **2 — Index / memory** | Word-window chunks, embeddings (`all-MiniLM-L6-v2`), **FAISS** L2, per-step traces | `data/chunks/*.json`, `data/embeddings/*.json`, `data/vectors/index.faiss`, `data/vectors/map.json`, `data/traces/` |
| **3 — Graph** | Structural **NEXT_CHUNK** edges from chunk order | `data/graphs/nodes.json`, `data/graphs/edges.json`, `data/graphs/traces/` |

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
2. `pdf-ingest` — writes Markdown + audit JSON (`configs/settings.yaml` paths for Phase 1).
3. `pdf-index` — word-window chunks, per-doc embedding JSON, global `index.faiss` + `map.json`, traces (`*_chunking`, `*_embedding`, `vectorstore`).
4. `pdf-graph` — builds `nodes.json` / `edges.json`.
5. `pdf-query "your question"` — JSON results over **`map.json` + local FAISS** (downloads the embedding model on first use).

## Honest limits

- **First index/query run** downloads **`all-MiniLM-L6-v2`** (network, disk). Pin versions in deployments if needed.
- **No OCR guarantee** beyond what extractors recover; scanned pages may yield little text.
- **FAISS** uses **`IndexFlatL2`** — exact, fine for small corpora.

## Development

```bash
pytest
ruff check .
```

## License

MIT — see `LICENSE`.
