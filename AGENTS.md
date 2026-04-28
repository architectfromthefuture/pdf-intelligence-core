# AGENTS

This repo is a minimal **observable document intelligence** pipeline. The public story is intentional, in order:

1. **Core Ingestion Engine**
2. **Indexing / Memory Layer**
3. **Deterministic Graph Structure**

That order positions the work as systems you can inspect and rebuild from artifacts—not “another PDF script.”

## Rule

Keep the system phase-based and inspectable.

Do not add LLM-generated graph edges, databases, APIs, dashboards, Docker, or cloud deployment unless explicitly requested.

## Core story

```txt
PDF
→ Markdown + audit
→ chunks + traces
→ embeddings + vector mapping
→ graph nodes/edges + provenance
```

## Design principles

- deterministic first
- trace every transformation
- preserve provenance
- prefer simple JSON artifacts before databases
- keep code readable
- do not hide behavior behind magic abstractions

## Phase boundaries

- **Phase 1:** ingestion only.
- **Phase 2:** indexing/memory only.
- **Phase 3:** graph structure only.

Do not mix graph logic into ingestion.

Do not read PDFs directly from graph code.

Graph must be reconstructable from chunk artifacts only.

## Entry points (console scripts)

| CLI | Module |
|-----|--------|
| `pdf-core-ingest` | `pdf_core.ingest.pipeline` |
| `pdf-core-index` | `pdf_core.index.pipeline` |
| `pdf-core-query` | `pdf_core.index.retriever` |
| `pdf-core-graph` | `pdf_core.graph.pipeline` |

Maintenance: when behavior changes, update tests and matching `docs/phase_*.md`. Keep `configs/settings.yaml` aligned with `pdf_core.config.load_settings()` for ingestion paths.

---

## Validation

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -e .
pytest
```

Optional smoke (when a sample PDF exists):

```bash
cp path/to/sample.pdf data/inbox/
pdf-core-ingest
pdf-core-index
pdf-core-query "test query"
pdf-core-graph

find data -maxdepth 3 -type f | sort
```

## Do not

- Add a web app or UI.
- Add FastAPI, Docker, or databases yet (unless explicitly requested).
- Add LLM graph extraction, OpenAI calls, or LangChain to the default pipeline.
- Add cloud deployment or dashboards.
- Overclaim that this is production RAG.
- Skip traces, audit records, or provenance fields.

---

## How this becomes website content later

After the GitHub repo exists and runs, turn each phase into a website documentation article:

```txt
/docs/pdf_core_ingestion_engine.html
/docs/indexing_memory_layer.html
/docs/deterministic_graph_structure.html
```

These are placeholders for a future publish step—not files this repository must ship.
