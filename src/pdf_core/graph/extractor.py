"""Project chunk JSON files into node records (deterministic, chunks only)."""

from __future__ import annotations

import json
from pathlib import Path

from pdf_core.graph.schema import NodeRecord


def load_chunk_files(chunks_dir: Path) -> list[Path]:
    return sorted(chunks_dir.glob("*.json"))


def nodes_from_chunk_file(path: Path) -> list[NodeRecord]:
    data = json.loads(path.read_text(encoding="utf-8"))
    doc_id = str(data.get("doc_id") or path.stem)
    chunks = data.get("chunks") or []

    def sort_key(ch: dict) -> tuple[int, str]:
        if "start_word" in ch:
            return (int(ch["start_word"]), str(ch.get("chunk_id", "")))
        return (int(ch.get("ord", 0)), str(ch.get("id", "") or ch.get("chunk_id", "")))

    sorted_chunks = sorted(chunks, key=sort_key)
    out: list[NodeRecord] = []
    for ord_i, ch in enumerate(sorted_chunks):
        if "chunk_id" in ch:
            cid_key = str(ch["chunk_id"])
            node_id = f"{doc_id}__{cid_key}"
        else:
            node_id = str(ch["id"])
        body = str(ch.get("text") or "")
        out.append(
            NodeRecord(
                id=node_id,
                type="CHUNK",
                doc_stem=doc_id,
                ord=ord_i,
                text_preview=body[:240].replace("\n", " "),
            )
        )
    return out


def extract_all(chunks_dir: Path) -> list[NodeRecord]:
    nodes: list[NodeRecord] = []
    for path in load_chunk_files(chunks_dir):
        nodes.extend(nodes_from_chunk_file(path))
    return nodes
