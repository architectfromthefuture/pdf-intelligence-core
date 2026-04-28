"""Minimal graph schema (JSON-serializable)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

NodeType = Literal["CHUNK"]
EdgeType = Literal["NEXT_CHUNK"]


@dataclass
class NodeRecord:
    id: str
    type: NodeType
    doc_stem: str
    ord: int
    text_preview: str


@dataclass
class EdgeRecord:
    id: str
    source: str
    target: str
    kind: EdgeType
    weight: float
