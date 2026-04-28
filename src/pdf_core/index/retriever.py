"""Retrieve top-k chunks using the FAISS index + meta sidecar."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from pdf_core.config import Settings
from pdf_core.index.embedder import encode_texts
from pdf_core.index.vectorstore import VectorMeta, load_index, load_meta


def retrieve(
    *,
    query: str,
    vectors_dir: Path,
    settings: Settings,
) -> list[tuple[float, VectorMeta]]:
    index_path = vectors_dir / "index.faiss"
    meta_path = vectors_dir / "meta.json"
    index = load_index(index_path)
    rows = load_meta(meta_path)
    q = encode_texts(
        [query],
        settings.embedding_dim,
        normalize=settings.embedding_normalize,
    )[0].reshape(1, -1)

    sims, idxs = index.search(q.astype(np.float32), settings.retrieve_top_k)
    hits: list[tuple[float, VectorMeta]] = []
    for score, ix in zip(sims[0].tolist(), idxs[0].tolist(), strict=True):
        if ix < 0 or ix >= len(rows):
            continue
        hits.append((float(score), rows[ix]))
    return hits
