"""FAISS-backed vector store with JSON sidecar metadata."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import faiss
import numpy as np


@dataclass(frozen=True)
class VectorMeta:
    chunk_id: str
    doc_stem: str
    ord: int
    text_preview: str


def build_index(vectors: np.ndarray) -> faiss.IndexFlatIP:
    if vectors.dtype != np.float32:
        vectors = vectors.astype(np.float32)
    dim = vectors.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(vectors)
    return index


def save_index(index: faiss.Index, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(path))


def load_index(path: Path) -> faiss.Index:
    return faiss.read_index(str(path))


def save_meta(rows: list[VectorMeta], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"records": [asdict(r) for r in rows]}
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def load_meta(path: Path) -> list[VectorMeta]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [VectorMeta(**rec) for rec in data["records"]]
