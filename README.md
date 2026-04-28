# pdf-intelligence-core

**One line:** A small, honest Python library that walks a PDF through a **phased** document-intelligence pipeline—ingestion, indexing, and a minimal graph projection—so you can ship a clear story without overclaiming.

## Status

- **Maturity:** experimental (alpha)
- **Production use:** no—use as a reference implementation and extension point

## Pipeline story

```txt
PDF
→ validated
→ extracted
→ normalized Markdown
→ audited
→ chunked
→ embedded
→ indexed
→ retrieved
→ projected into graph structure
```

Phases are mapped to code as:

| Phase | Focus | Modules |
|-------|--------|---------|
| **1** — Core ingestion | validate, extract, normalize, audit | `pdf_intelligence_core.phase1` |
| **2** — Indexing / memory | chunk, embed, index, retrieve | `pdf_intelligence_core.phase2` |
| **3** — Graph / structure | project nodes and edges over chunks | `pdf_intelligence_core.phase3` |

See `docs/PIPELINE.md` for contracts and boundaries.

## What this is

- **In scope:** Sequential pipeline API (`run_pipeline`), pluggable embeddings (`Embedder` protocol), in-memory brute-force retrieval (`MemoryVectorIndex`), and a readable `DocumentGraph` (sequential **NEXT_CHUNK** edges plus optional **SIMILAR** cosine edges).

- **Primary artifacts:** importable Python package and optional CLI `pdf-intelligence`.

## What this is not

- Not OCR or layout reconstruction for scanned documents (extract is **embedded text via pypdf**).
- Not a production vector database or approximate nearest-neighbor tier at scale—the index is intentional **brute-force** for clarity and testing.
- Not SOTA embeddings by default—the bundled `HashEmbedder` exists for deterministic offline use; swap in a real model when quality matters.

## Honest scope (anti–overfitting)

**This repository does not claim:**

- Production readiness without runbooks, security review, and evals you add yourself.
- Semantic retrieval quality when using `HashEmbedder` (it is not a neural model).
- Parity with closed commercial document-AI stacks.

**Evidence posture**

- **Verified here:** `pytest` for validation, chunking, pipeline wiring, and graph projection.
- **Described but not verified:** anything you build on top (external embedders, graph DBs, OCR).

## Quickstart

```bash
cd pdf-intelligence-core
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

Run the CLI on a PDF:

```bash
pip install -e .
pdf-intelligence path/to/file.pdf --query "What is this about?"
pdf-intelligence path/to/file.pdf --json
```

From Python:

```python
from pathlib import Path
from pdf_intelligence_core import run_pipeline

result = run_pipeline(Path("paper.pdf").read_bytes(), query="methods section")
print(result.retrieval_sample[0][1].text[:500])
```

## Design notes

- **Core idea:** Treat each stage as a **pure contract** (bytes in / structured artifacts out) so you can replace extractors, embedders, or the index without rewriting the story.
- **Limits:** Image-only PDFs yield empty extract; long documents need a real ANN index and batching; graph edges are **heuristic** (sequence + embedding similarity), not logical PDF structure.

## Contributing

See `CONTRIBUTING.md`.

## License

MIT — see `LICENSE`.

## Security

See `SECURITY.md`.
