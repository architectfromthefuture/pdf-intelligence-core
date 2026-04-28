```txt
data/inbox/*.pdf
    └─ pdf-ingest
        ├─ data/markdown/*.md
        └─ data/audit/*.json

data/markdown/*.md
    └─ pdf-index
        ├─ data/chunks/*.json           (doc_id + word-window chunks)
        ├─ data/embeddings/*.json       (SentenceTransformer vectors + traces)
        ├─ data/vectors/index.faiss      (Faiss.IndexFlatL2)
        ├─ data/vectors/map.json        (uuid ↔ chunk_id ↔ full text)
        ├─ data/traces/{doc}_chunking.json
        ├─ data/traces/{doc}_embedding.json
        └─ data/traces/vectorstore.json

data/chunks/*.json
    └─ pdf-graph
        ├─ data/graphs/nodes.json
        ├─ data/graphs/edges.json
        └─ data/graphs/traces/graph_last.json

pdf-query …
    └─ uses data/vectors/index.faiss + map.json after indexing
```

### Configuration

Phase 1 path overrides still live in `configs/settings.yaml`. Phase 2 indexing resolves `data/` via the repository root (`repo_root()`), matching the CLI layouts above.

### Design principles

- **Inspectability** — Any stage can be read as JSON, Markdown, or on-disk indices.
- **Traces per transform** — Chunking, embedding, and vector persisting each emit `data/traces/*.json`.
- **Swappable knobs** — `run_indexing(chunk_size=…)` adjusts the word window; swapping the embedding model starts in `pdf_core/index/embedder.py`.
