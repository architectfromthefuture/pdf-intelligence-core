# Architecture

```txt
data/inbox/*.pdf
    └─ pdf-ingest
        ├─ data/markdown/*.md
        └─ data/audit/*.json

data/markdown/*.md
    └─ pdf-index
        ├─ data/chunks/*.json        (per-document chunk bundles)
        ├─ data/embeddings/matrix.npy  (float32 [N, dim])
        ├─ data/vectors/index.faiss     (FAISS flat inner-product)
        ├─ data/vectors/meta.json       (row ↔ chunk id)
        └─ data/traces/index_last.json

data/chunks/*.json
    └─ pdf-graph
        ├─ data/graphs/nodes.json
        ├─ data/graphs/edges.json
        └─ data/graphs/traces/graph_last.json

pdf-query
    └─ reads data/vectors/* (after index build)
```

### Configuration

Paths and hyperparameters live in `configs/settings.yaml` and are resolved against the **repository root** by `pdf_core.config.load_settings`.

### Design principles

- **Inspectability** — Any stage can be read as JSON/Markdown/binary FAISS/NPY on disk.
- **No hidden services** — Retrieval and graph steps work fully offline with declared dependencies.
- **Swappable core** — Embedder and FAISS index class are the main extension points without rewriting the phase story.
