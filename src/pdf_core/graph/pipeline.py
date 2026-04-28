"""Chunks → deterministic graph → ``nodes.json`` / ``edges.json``."""

from __future__ import annotations

from pdf_core.config import Settings, load_settings
from pdf_core.graph.builder import build_next_chunk_edges
from pdf_core.graph.extractor import extract_all
from pdf_core.graph.store import write_graph
from pdf_core.graph.trace import write_graph_trace


def run_graph_pipeline(*, settings: Settings | None = None) -> None:
    settings = settings or load_settings()

    nodes = extract_all(settings.chunks)
    edges = build_next_chunk_edges(nodes)

    npath, epath = write_graph(nodes, edges, settings.graphs)

    trace = {
        "phase": "graph",
        "node_count": len(nodes),
        "edge_count": len(edges),
        "artifacts": {
            "nodes": str(npath),
            "edges": str(epath),
        },
    }
    write_graph_trace(trace, settings.graph_traces)

    print(f"[OK] graph: {len(nodes)} nodes, {len(edges)} edges → {settings.graphs}")
