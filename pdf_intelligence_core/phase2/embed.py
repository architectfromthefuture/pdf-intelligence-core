"""Pluggable embeddings: default deterministic embedding for offline use."""

from __future__ import annotations

import hashlib
import math
from typing import Protocol, runtime_checkable


def _clamp11(x: float) -> float:
    return max(-1.0, min(1.0, x))


@runtime_checkable
class Embedder(Protocol):
    """Maps text to dense vectors for retrieval."""

    dim: int

    def encode(self, texts: list[str]) -> list[list[float]]: ...


def _encode_one_sha256_hex(text: str, dim: int) -> list[float]:
    blob = hashlib.sha256(text.encode("utf-8")).digest()
    vals: list[float] = []
    while len(vals) < dim:
        for i in range(0, len(blob) - 1, 2):
            vals.append(_clamp11(int.from_bytes(blob[i : i + 2], "big") / 65535.0 * 2 - 1))
            if len(vals) >= dim:
                break
        blob = hashlib.sha256(blob).digest()
    n = math.sqrt(sum(x * x for x in vals)) or 1.0
    return [x / n for x in vals]


class HashEmbedder:
    """
    Deterministic pseudo-embeddings derived from UTF-8 + SHA-256.

    Intended for CI/tests and demos without heavyweight models. Swap for
    sentence-transformers or hosted APIs when semantic quality matters.
    """

    dim: int = 64

    def encode(self, texts: list[str]) -> list[list[float]]:
        return [_encode_one_sha256_hex(t, self.dim) for t in texts]
