# Phase 3 — Graph structure

Inputs: **`data/chunks/*.json` only** (word-window payloads from indexing). No PDF reload, **no embeddings passed in**, **no LLM edge synthesis**.

Per chunk (`doc_id`, `chunk_id`, `text`), the pipeline:

1. Runs **`regex_capital_phrase`** to collect multi-token capital phrases (ordered, unique).
2. Emits **nodes**: one `(entity × chunk)` — id `"{entity}:{doc_id}:{chunk_id}"`-style labeling with `doc_id:` + logical chunk id preserved in **`source_chunk_id`** as `"{doc_id}:{chunk_id}"`.
3. Emits **`co_occurs_in` edges**: every unordered distinct pair `(entity_i, entity_j)` inside the **same chunk text**, stamped with `source_chunk_id` and **`doc_id`**.

Writes:

- **`data/graphs/nodes.json`**, **`data/graphs/edges.json`**, **`data/graphs/graph_index.json`** (counts + paths).
- **`data/graphs/traces/<doc_id>_chunk_<id>.json`** — method, extracted entities, edge count — one trace per indexed chunk occurrence.
