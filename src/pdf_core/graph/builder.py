"""Pairwise co-occurrence edges for entities appearing in the same chunk."""

from __future__ import annotations

import uuid
from typing import Any


def build_relations(entities: list[str], chunk_id: str) -> list[dict[str, Any]]:
    edges: list[dict[str, Any]] = []

    for index, source in enumerate(entities):
        for target in entities[index + 1 :]:
            edges.append(
                {
                    "id": str(uuid.uuid4()),
                    "source": source,
                    "target": target,
                    "relation": "co_occurs_in",
                    "source_chunk_id": chunk_id,
                }
            )

    return edges
