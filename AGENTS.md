# AGENTS — `pdf-intelligence-core`

## Intent

Preserve a **narrow, reproducible** document pipeline: ingestion → chunked index → deterministic graph artifacts. Prefer **truthful, inspectable files** over feature sprawl.

## Do

- Keep paths consistent with `configs/settings.yaml` and `pdf_core.config.load_settings()`.
- When changing behavior, update **tests** and the relevant `docs/phase_*.md` summary.
- Treat `data/` as local run output; never commit secrets or private PDFs.

## Do not

- Add a web app, Docker, cloud infra, external databases, or LLM API calls in the default path without an explicit project decision.
- Paste large raw design notes into `README.md`—summarize in `docs/` instead.

## Useful entrypoints

| CLI | Module |
|-----|--------|
| `pdf-ingest` | `pdf_core.ingest.pipeline` |
| `pdf-index` | `pdf_core.index.pipeline.run_indexing` |
| `pdf-graph` | `pdf_core.graph.pipeline` |
| `pdf-query` | `pdf_core.index.retriever` |
