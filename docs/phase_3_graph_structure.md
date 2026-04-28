# Phase 3 — Graph / structure

Phase 3 reads chunk JSON from `data/chunks/` and emits a **deterministic** graph using **chunk metadata only**—chiefly reading order.

## Nodes

Each chunk becomes a node (`type=CHUNK`) with `doc_stem`, ordinals, and a short preview derived from the chunk text.

## Edges

Within each document (grouped by `stem`), consecutive chunks connect with **`NEXT_CHUNK`** edges (weight 1.0). No LLM, no external APIs, no stochastic layout inference.

## Artifacts

- `data/graphs/nodes.json`
- `data/graphs/edges.json`
- `data/graphs/traces/graph_last.json`

## CLI

`pdf-graph` rebuilds the graph whenever chunk files change.
