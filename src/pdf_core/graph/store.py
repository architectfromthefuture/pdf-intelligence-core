"""JSON graph artifacts on disk."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pdf_core.config import repo_root


def graphs_dir() -> Path:
    return repo_root() / "data/graphs"


def nodes_json_path() -> Path:
    return graphs_dir() / "nodes.json"


def edges_json_path() -> Path:
    return graphs_dir() / "edges.json"


def graph_index_path() -> Path:
    return graphs_dir() / "graph_index.json"


def save_graph(nodes: list[dict[str, Any]], edges: list[dict[str, Any]]) -> dict[str, Any]:
    gd = graphs_dir()
    gd.mkdir(parents=True, exist_ok=True)
    np = nodes_json_path()
    ep = edges_json_path()
    ip = graph_index_path()

    np.write_text(json.dumps(nodes, indent=2), encoding="utf-8")
    ep.write_text(json.dumps(edges, indent=2), encoding="utf-8")

    index = {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "node_path": str(np),
        "edge_path": str(ep),
    }

    ip.write_text(json.dumps(index, indent=2), encoding="utf-8")

    return index