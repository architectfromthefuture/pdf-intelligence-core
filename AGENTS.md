# AGENTS — `pdf-intelligence-core`

## Intent

Keep a **narrow, reproducible** document pipeline: ingestion → chunked index → embeddings/FAISS → **deterministic graph from chunk text**. Prefer **truthful artifacts on disk** over feature sprawl.

## Do

- Preserve **Phase 3 invariants**: no PDF ingress, no embeddings, no LLM edges — only **`data/chunks/*.json`**.
- When changing behavior, update **tests** and the matching `docs/phase_*.md` section.
- Keep `configs/settings.yaml` consistent with **`pdf_core.config.load_settings()`** for ingestion paths.

## Do not

- Add a web UI, Docker, hosted DBs, or LLM-based graph construction in the default path without an explicit project decision.
- Paste raw design notes into `README.md` — summarize in `docs/`.

## Entry points (console scripts)

| CLI | Module |
|-----|--------|
| `pdf-core-ingest` | `pdf_core.ingest.pipeline` |
| `pdf-core-index` | `pdf_core.index.pipeline` |
| `pdf-core-query` | `pdf_core.index.retriever` |
| `pdf-core-graph` | `pdf_core.graph.pipeline` |
