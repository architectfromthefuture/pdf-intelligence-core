# Architecture

```txt
PDF
→ Phase 1: ingestion → Markdown (`data/markdown/*.md`) + audit (`data/audit/*.json`)

Markdown
→ Phase 2: indexing → chunk JSON (`data/chunks/*.json`) → embedding JSON (`data/embeddings/*.json`)
   → traces (`data/traces/*.json`)
   → Faiss.IndexFlatL2 + map (`data/vectors/index.faiss`, `data/vectors/map.json`)

Indexing + vectors
→ Phase 2 query: `pdf-core-query …` resolves rows through `map.json` + Faiss index

Chunks (`data/chunks/*.json` alone)
→ Phase 3: graph projection → deterministic regex entities → pairwise `co_occurs_in` edges within each chunk
   → `nodes.json`, `edges.json`, `graph_index.json`, traces under `data/graphs/traces/`
```

Phase 3 **does not** open PDF bytes, embedding matrices, or any LLM. It consumes only persisted chunk payloads so the structure is reproducible and inspectable end-to-end.

`configs/settings.yaml` remains the source for Phase 1 path layout; Phase 2/3 indexing and graph artifacts resolve under `repo_root()` / `data/…`.
