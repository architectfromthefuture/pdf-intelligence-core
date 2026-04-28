# Phase 1 — Core ingestion

Phase 1 turns PDFs in `data/inbox/` into **normalized Markdown** plus **structured audit JSON**.

## Steps

1. **Validate** — PyMuPDF opens the file, counts pages, computes a SHA-256 digest of bytes.
2. **Extract** — Prefer `pymupdf4llm.to_markdown` for structured text; on failure, fall back to `pdfplumber` page text and record the reason.
3. **Normalize** — Collapse whitespace, join hyphenated line breaks, deduplicate exact repeated lines (lossy by design for noisy PDFs).
4. **Persist** — Markdown under `data/markdown/{stem}.md`; audit under `data/audit/{stem}.json` with timestamp.

## CLI

`pdf-core-ingest` invokes `run_pipeline()` and processes every `*.pdf` found in the inbox.

## Operational notes

- Outputs are **artifact-first**: you can diff Markdown and audit files between runs.
- This phase does **not** OCR raster pages; image-only PDFs often yield empty or thin text.
