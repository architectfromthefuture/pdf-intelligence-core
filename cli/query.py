"""Query the local FAISS index (requires prior ``pdf-index`` run)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from pdf_core.config import repo_root
from pdf_core.index.retriever import INDEX_PATH, MAP_PATH, search


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Retrieve top-k matches from map.json / index.faiss.")
    parser.add_argument("query")
    parser.add_argument("-k", type=int, default=5)

    args = parser.parse_args(argv)

    idx = Path(INDEX_PATH)
    mpath = Path(MAP_PATH)
    if not idx.exists() or not mpath.exists():
        repo = repo_root()
        print(f"No index under {repo / 'data/vectors'}. Run `pdf-core-index` after `pdf-core-ingest`.", file=sys.stderr)
        raise SystemExit(2)

    result = search(args.query, k=args.k)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
