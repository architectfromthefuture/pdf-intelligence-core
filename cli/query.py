"""Query the local FAISS index (requires prior ``pdf-index`` run)."""

from __future__ import annotations

import argparse
import sys

from pdf_core.config import load_settings
from pdf_core.index.retriever import retrieve


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Retrieve top-k chunks from the local FAISS index.")
    parser.add_argument("query", nargs="?", default="overview", help="Natural language query string")
    args = parser.parse_args(argv)

    settings = load_settings()
    idx_path = settings.vectors / "index.faiss"
    meta_path = settings.vectors / "meta.json"
    if not idx_path.exists() or not meta_path.exists():
        print("No local index found. Run `pdf-index` after `pdf-ingest`.", file=sys.stderr)
        raise SystemExit(2)

    hits = retrieve(query=args.query, vectors_dir=settings.vectors, settings=settings)
    print(f'Query: "{args.query}" — {len(hits)} hits')
    for score, row in hits:
        print(f"[{score:.4f}] {row.chunk_id} ({row.doc_stem}) — {row.text_preview}")


if __name__ == "__main__":
    main()
