# Phase 2 — Indexing / memory

Phase 2 reads Markdown from `data/markdown/`, emits **chunks**, **sentence embeddings**, a **global FAISS** index + **mapping JSON**, and a **trace file for every transformation**.

## Chunking (`fixed_word_window`)

`chunk_text` splits normalized text on whitespace into word lists, then emits fixed-length windows (`chunk_size` words, default 500). Each window keeps a stable **`chunk_id`** (`chunk_0000`, …), **`start_word` / `end_word`**, and the joined text—so downstream graph provenance stays explicit.

## Embeddings

`embed_chunks` uses **`sentence_transformers`** with **`all-MiniLM-L6-v2`**. Each chunk gets:

- one **uuid** (`id`) for the stored vector row
- **`chunk_id`** copied from chunking for cross-artifact linkage
- a **parallel trace** payload (preview, model id, indexes)

Artifacts: `data/embeddings/{doc_id}.json` (vectors + trace + model name).

## Vector store

`build_index` stacks all embedding vectors across documents into **`faiss.IndexFlatL2`**, writes **`data/vectors/index.faiss`**, and **`data/vectors/map.json`** with `{ "ids": [...], "records": [...] }` where each record holds `vector_id`, `chunk_id`, and full **`text`** for round-tripping.

## Tracing (required)

Every step writes JSON under **`data/traces/`**:

| Trace file | Meaning |
|------------|---------|
| `{doc}_chunking` | Strategy, window size, count, chunk file path |
| `{doc}_embedding` | Model, vector count, embedding file path |
| `vectorstore` | FAISS path, map path, dims, totals |

## Query

`search(query, k)` embeds the query with the **same model**, runs FAISS, and resolves rows through **`map.json`**. The `pdf-query` CLI prints **`json.dumps`**.

## Operational notes

- Empty Markdown yields **zero** chunks; embedding files may be empty lists; **`vectorstore`** trace records `count: 0` if nothing was indexed.
- Run commands from **any cwd**—paths resolve to the repo root via **`pdf_core.config.repo_root()`**.
