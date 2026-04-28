"""Build graph JSON from chunk artifacts only — no PDF, vectors, or LLMs."""

from __future__ import annotations

import json

from pdf_core.config import repo_root
from pdf_core.graph.builder import build_relations
from pdf_core.graph.extractor import extract_entities
from pdf_core.graph.store import save_graph
from pdf_core.graph.trace import write_trace


def run_graph_pipeline() -> None:
    all_nodes: list[dict] = []
    all_edges: list[dict] = []

    chunk_files = sorted((repo_root() / "data/chunks").glob("*.json"))

    if not chunk_files:
        print("No chunk files found in data/chunks/")
        return

    seen_nodes: set[tuple[str, str]] = set()

    for file in chunk_files:
        chunk_data = json.loads(file.read_text(encoding="utf-8"))
        doc_id = chunk_data.get("doc_id", file.stem)

        for chunk in chunk_data["chunks"]:
            chunk_id = f"{doc_id}:{chunk['chunk_id']}"
            text = chunk["text"]

            result = extract_entities(text)
            entities = result["entities"]

            for entity in entities:
                node_key = (entity, chunk_id)

                if node_key not in seen_nodes:
                    all_nodes.append(
                        {
                            "id": f"{entity}:{chunk_id}",
                            "label": entity,
                            "source_chunk_id": chunk_id,
                            "doc_id": doc_id,
                        }
                    )
                    seen_nodes.add(node_key)

            edges = build_relations(entities, chunk_id)

            for edge in edges:
                edge["doc_id"] = doc_id

            all_edges.extend(edges)

            write_trace(
                chunk_id.replace(":", "_"),
                {
                    "doc_id": doc_id,
                    "chunk_id": chunk_id,
                    "method": result["method"],
                    "entities": entities,
                    "edge_count": len(edges),
                },
            )

    graph_index = save_graph(all_nodes, all_edges)

    print(
        f"[GRAPH BUILT] nodes={graph_index['node_count']} edges={graph_index['edge_count']}"
    )

