"""SentenceTransformer embeddings over chunk dictionaries."""

from __future__ import annotations

import uuid
from typing import Any

from sentence_transformers import SentenceTransformer


_MODEL_NAME = "all-MiniLM-L6-v2"
_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    global _model

    if _model is None:
        _model = SentenceTransformer(_MODEL_NAME)

    return _model


def embed_chunks(chunks: list[dict[str, Any]]) -> dict[str, Any]:
    if not chunks:
        return {
            "vectors": [],
            "trace": [],
            "model": _MODEL_NAME,
        }

    model = get_model()

    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts)

    trace: list[dict[str, Any]] = []
    vectors: list[dict[str, Any]] = []

    for index, chunk in enumerate(chunks):
        vector_id = str(uuid.uuid4())

        vectors.append(
            {
                "id": vector_id,
                "embedding": embeddings[index].tolist(),
                "text": chunk["text"],
                "chunk_id": chunk["chunk_id"],
            }
        )

        trace.append(
            {
                "vector_id": vector_id,
                "chunk_id": chunk["chunk_id"],
                "chunk_index": index,
                "text_preview": chunk["text"][:120],
                "model": _MODEL_NAME,
            }
        )

    return {
        "vectors": vectors,
        "trace": trace,
        "model": _MODEL_NAME,
    }
