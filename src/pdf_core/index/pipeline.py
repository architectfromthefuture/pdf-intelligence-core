"""Indexing pipeline: Markdown → chunks → embeddings → FAISS (each step traced)."""

from __future__ import annotations

import json

from pdf_core.config import repo_root
from pdf_core.index.chunker import chunk_text
from pdf_core.index.embedder import embed_chunks
from pdf_core.index.trace import write_trace
from pdf_core.index.vectorstore import build_index

MARKDOWN = repo_root() / "data/markdown"
CHUNK_DIR = repo_root() / "data/chunks"
EMBEDDING_DIR = repo_root() / "data/embeddings"


def run_indexing(chunk_size: int = 500) -> None:
    CHUNK_DIR.mkdir(parents=True, exist_ok=True)
    EMBEDDING_DIR.mkdir(parents=True, exist_ok=True)

    markdown_files = sorted(MARKDOWN.glob("*.md"))

    if not markdown_files:
        print("No markdown files found in data/markdown/")
        return

    all_vectors: list[dict] = []

    for file in markdown_files:
        text = file.read_text(encoding="utf-8")

        chunk_result = chunk_text(text, chunk_size=chunk_size)

        chunk_payload = {
            "doc_id": file.stem,
            **chunk_result,
        }

        chunk_path = CHUNK_DIR / f"{file.stem}.json"
        chunk_path.write_text(json.dumps(chunk_payload, indent=2), encoding="utf-8")

        write_trace(
            f"{file.stem}_chunking",
            {
                "doc_id": file.stem,
                "strategy": chunk_result["strategy"],
                "chunk_size": chunk_result["chunk_size"],
                "chunk_count": chunk_result["total_chunks"],
                "chunk_file": str(chunk_path),
            },
        )

        embed_result = embed_chunks(chunk_result["chunks"])

        embedding_path = EMBEDDING_DIR / f"{file.stem}.json"
        embedding_path.write_text(json.dumps(embed_result, indent=2), encoding="utf-8")

        write_trace(
            f"{file.stem}_embedding",
            {
                "doc_id": file.stem,
                "model": embed_result["model"],
                "count": len(embed_result["vectors"]),
                "embedding_file": str(embedding_path),
            },
        )

        all_vectors.extend(embed_result["vectors"])

        print(f"[INDEXED] {file.name}")

    index_result = build_index(all_vectors)

    write_trace("vectorstore", index_result)


# Backward-compatible name for older imports
run_index_pipeline = run_indexing
