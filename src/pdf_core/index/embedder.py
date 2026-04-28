"""Lightweight deterministic embeddings (no external inference API)."""

from __future__ import annotations

import hashlib
from typing import Sequence

import numpy as np


def _unit(vec: np.ndarray) -> np.ndarray:
    n = float(np.linalg.norm(vec)) or 1.0
    return (vec / n).astype(np.float32)


def encode_texts(texts: Sequence[str], dim: int, *, normalize: bool = True) -> np.ndarray:
    """Map each string to a normalized float32 vector of shape (len(texts), dim)."""
    rows: list[np.ndarray] = []
    for t in texts:
        blob = hashlib.sha256(t.encode("utf-8")).digest()
        vals: list[float] = []
        while len(vals) < dim:
            for i in range(0, len(blob) - 1, 2):
                v = int.from_bytes(blob[i : i + 2], "big") / 65535.0 * 2.0 - 1.0
                vals.append(max(-1.0, min(1.0, v)))
                if len(vals) >= dim:
                    break
            blob = hashlib.sha256(blob).digest()
        arr = np.asarray(vals[:dim], dtype=np.float32)
        if normalize:
            arr = _unit(arr)
        rows.append(arr)
    return np.stack(rows, axis=0)
