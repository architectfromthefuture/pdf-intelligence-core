"""FAISS L2 index + JSON mapping (vector → chunk → text)."""

from __future__ import annotations

import json
from typing import Any

import faiss
import numpy as np

from pdf_core.config import repo_root


VECTOR_DIR = repo_root() / "data/vectors"
INDEX_PATH = VECTOR_DIR / "index.faiss"
MAP_PATH = VECTOR_DIR / "map.json"


def build_index(vectors: list[dict[str, Any]]) -> dict[str, Any]:
    if not vectors:
        return {"count": 0, "dim": 0}

    VECTOR_DIR.mkdir(parents=True, exist_ok=True)

    dim = len(vectors[0]["embedding"])
    index = faiss.IndexFlatL2(dim)

    ids: list[str] = []
    records: list[dict[str, str]] = []
    matrix: list[list[float]] = []

    for vector in vectors:
        ids.append(vector["id"])
        matrix.append(vector["embedding"])
        records.append(
            {
                "vector_id": vector["id"],
                "chunk_id": vector["chunk_id"],
                "text": vector["text"],
            }
        )

    stacked = np.array(matrix).astype("float32")
    index.add(stacked)

    faiss.write_index(index, str(INDEX_PATH))

    MAP_PATH.write_text(
        json.dumps(
            {
                "ids": ids,
                "records": records,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    return {
        "count": len(vectors),
        "dim": dim,
        "index_path": str(INDEX_PATH),
        "map_path": str(MAP_PATH),
    }
