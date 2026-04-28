# pdf-intelligence-core

**Public story — in order:**

1. **Core Ingestion Engine**
2. **Indexing / Memory Layer**
3. **Deterministic Graph Structure**

That framing is deliberate. It reads less like “I made a PDF tool” and more like **I’m building observable document intelligence from first principles**—each phase adds structure you can open, diff, and rebuild from artifacts.

This repo walks that path: PDFs become Markdown and audits, Markdown becomes chunks and traces, chunks become embeddings and a searchable vector map, then chunk files alone yield a deterministic graph with provenance.

## Artifact flow

```txt
PDF
→ Markdown + audit
→ chunks + trace
→ embeddings + trace
→ vector index + mapping
→ graph nodes/edges + provenance
```

## Phases (same narrative)

### 1 — Core Ingestion Engine

PDF → validated → extracted → normalized → Markdown + audit.

### 2 — Indexing / Memory Layer

Markdown → chunks → embeddings → FAISS index + trace artifacts.

### 3 — Deterministic Graph Structure

Chunks → regex entities → co-occurrence relationships → graph JSON + per-chunk provenance traces — **from chunk text only** (no raw PDF reads, no embedding vectors passed into the graph, no LLM edge generation).

## Why not “jump straight to vectors”?

Most pipelines bury the early steps; this one keeps **every transformation visible** so you can inspect and reproduce behavior without trusting a black box.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
```

## Docker runtime

Run the pipeline in a container while `./data/` on the host stays the **persistent artifact layer** (same layout as native runs). Reproducibility: pinned base image + `requirements.txt` + editable install; **no** baked `data/` blobs in the image.

```bash
docker compose build
docker compose up -d
docker exec -it pdf_intelligence_core bash

python -m cli ingest
python -m cli index
python -m cli query "what is this document about?"
python -m cli graph

docker compose down
```

Details: **`docs/docker_runtime.md`**.

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
