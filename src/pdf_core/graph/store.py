"""Persist graph JSON next to other run artifacts."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from pdf_core.graph.schema import EdgeRecord, NodeRecord


def write_graph(nodes: list[NodeRecord], edges: list[EdgeRecord], graphs_dir: Path) -> tuple[Path, Path]:
    graphs_dir.mkdir(parents=True, exist_ok=True)
    nodes_path = graphs_dir / "nodes.json"
    edges_path = graphs_dir / "edges.json"
    nodes_path.write_text(json.dumps([asdict(n) for n in nodes], indent=2), encoding="utf-8")
    edges_path.write_text(json.dumps([asdict(e) for e in edges], indent=2), encoding="utf-8")
    return nodes_path, edges_path
