"""Markdown → chunks → embeddings → FAISS + trace artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np

from pdf_core.config import Settings, load_settings
from pdf_core.index.chunker import chunk_markdown_file
from pdf_core.index.embedder import encode_texts
from pdf_core.index.trace import write_trace
from pdf_core.index.vectorstore import VectorMeta, build_index, save_index, save_meta


def _write_chunk_file(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def run_index_pipeline(*, settings: Settings | None = None) -> None:
    settings = settings or load_settings()
    settings.markdown.mkdir(parents=True, exist_ok=True)

    md_files = sorted(settings.markdown.glob("*.md"))
    if not md_files:
        print("No Markdown files in data/markdown/. Run pdf-ingest first.")
        return

    all_rows: list[VectorMeta] = []
    texts_for_vecs: list[str] = []

    for md in md_files:
        payload = chunk_markdown_file(
            md,
            max_chars=settings.chunk_max_chars,
            overlap=settings.chunk_overlap_chars,
        )
        out_path = settings.chunks / f"{payload['stem']}.json"
        _write_chunk_file(out_path, payload)
        for ch in payload["chunks"]:
            all_rows.append(
                VectorMeta(
                    chunk_id=ch["id"],
                    doc_stem=payload["stem"],
                    ord=int(ch["ord"]),
                    text_preview=ch["text"][:200],
                )
            )
            texts_for_vecs.append(ch["text"])

    if not texts_for_vecs:
        print("No chunks produced.")
        return

    vecs = encode_texts(
        texts_for_vecs,
        settings.embedding_dim,
        normalize=settings.embedding_normalize,
    )
    settings.embeddings.mkdir(parents=True, exist_ok=True)
    np.save(settings.embeddings / "matrix.npy", vecs)

    index = build_index(vecs)
    settings.vectors.mkdir(parents=True, exist_ok=True)
    save_index(index, settings.vectors / "index.faiss")
    save_meta(all_rows, settings.vectors / "meta.json")

    trace = {
        "phase": "indexing",
        "markdown_files": [m.name for m in md_files],
        "chunk_count": len(texts_for_vecs),
        "embedding_dim": settings.embedding_dim,
        "artifacts": {
            "chunks_dir": str(settings.chunks),
            "embeddings_matrix": str(settings.embeddings / "matrix.npy"),
            "faiss_index": str(settings.vectors / "index.faiss"),
            "vector_meta": str(settings.vectors / "meta.json"),
        },
    }
    write_trace(trace, settings.traces, "index_last")
    print(f"[OK] indexed {len(texts_for_vecs)} chunks into FAISS.")
