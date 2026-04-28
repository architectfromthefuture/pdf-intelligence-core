"""Search the local FAISS index built by ``build_index`` (map.json sidecar)."""

from __future__ import annotations

import json
from typing import Any

import faiss
from sentence_transformers import SentenceTransformer

from pdf_core.config import repo_root


INDEX_PATH = repo_root() / "data/vectors/index.faiss"
MAP_PATH = repo_root() / "data/vectors/map.json"
_MODEL_NAME = "all-MiniLM-L6-v2"


def load_index():
    return faiss.read_index(str(INDEX_PATH))


def load_map() -> dict[str, Any]:
    return json.loads(MAP_PATH.read_text(encoding="utf-8"))


def search(query: str, k: int = 5) -> dict[str, Any]:
    model = SentenceTransformer(_MODEL_NAME)
    index = load_index()
    mapping = load_map()

    q_vec = model.encode([query]).astype("float32")

    distances, indices = index.search(q_vec, k)

    results: list[dict[str, Any]] = []

    records = mapping["records"]

    for rank, vec_idx in enumerate(indices[0]):
        if vec_idx < 0:
            continue

        record = records[int(vec_idx)]

        results.append(
            {
                "rank": rank + 1,
                "vector_id": record["vector_id"],
                "chunk_id": record["chunk_id"],
                "distance": float(distances[0][rank]),
                "text_preview": record["text"][:300],
            }
        )

    return {
        "query": query,
        "model": _MODEL_NAME,
        "results": results,
    }
