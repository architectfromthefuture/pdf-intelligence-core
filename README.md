# pdf-intelligence-core

A minimal, observable document intelligence pipeline.

This repo turns PDFs into Markdown, Markdown into chunks, chunks into embeddings, embeddings into a searchable vector index, and chunks into a deterministic graph structure.

## Why this exists

Most document pipelines jump from PDF straight into embeddings. That makes the system hard to inspect.

This project keeps every transformation visible:

```txt
PDF
→ Markdown + audit
→ chunks + trace
→ embeddings + trace
→ vector index + mapping
→ graph nodes/edges + provenance
```

## Phases

### Phase 1 — Core ingestion engine

PDF → validated → extracted → normalized → Markdown + audit.

### Phase 2 — Indexing / memory layer

Markdown → chunks → embeddings → FAISS index + trace artifacts.

### Phase 3 — Graph structure layer

Chunks → regex entities → co-occurrence relationships → graph JSON + per-chunk provenance traces — **from chunk text only** (no raw PDF reads, no embedding vectors passed into the graph, no LLM edge generation).

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
```

## Run ingestion

```bash
mkdir -p data/inbox
cp path/to/file.pdf data/inbox/
pdf-core-ingest
```

Outputs:

- `data/markdown/file.md`
- `data/audit/file.json`

## Run indexing

```bash
pdf-core-index
```

Outputs:

- `data/chunks/file.json`
- `data/embeddings/file.json`
- `data/vectors/index.faiss`
- `data/vectors/map.json`
- `data/traces/*.json`

## Query

```bash
pdf-core-query "what is this document about?"
```

## Build graph

```bash
pdf-core-graph
```

Outputs:

- `data/graphs/nodes.json`
- `data/graphs/edges.json`
- `data/graphs/graph_index.json`
- `data/graphs/traces/*.json`

Paths resolve from the repository root regardless of shell directory.

## Design principles

- **Deterministic first** — same chunks → same graph (regex-based entities, enumerated co-edges).
- **Observable transformations** — JSON/Markdown/FAISS on disk.
- **No hidden black boxes** — traces on chunk and embedding steps (Phase 2), per chunk (Phase 3).
- **Every artifact rebuildable** — pipeline steps are repeatable from stored inputs.
- **Every edge should have provenance** — edges carry `source_chunk_id`; nodes carry provenance ids.
- **No LLM-generated graph edges in v0.1.**

## What this is not

- Not a production RAG platform.
- Not a full knowledge graph system.
- Not an LLM reasoning engine.
- Not a UI.

It is the core pipeline skeleton.

## Roadmap

- Phase 4 — CLI/query polish, richer chunking strategies, richer metadata, graph inspection commands, evaluation harness, optional downstream LLM cleanup **above** these artifacts — not wired into Phase 3 edge construction today.

## License

MIT — see `LICENSE`.
