"""Project chunk JSON files into node records (deterministic, chunks only)."""

from __future__ import annotations

import json
from pathlib import Path

from pdf_core.graph.schema import NodeRecord


def load_chunk_files(chunks_dir: Path) -> list[Path]:
    return sorted(chunks_dir.glob("*.json"))


def nodes_from_chunk_file(path: Path) -> list[NodeRecord]:
    data = json.loads(path.read_text(encoding="utf-8"))
    stem = str(data.get("stem") or path.stem)
    chunks = data.get("chunks") or []
    out: list[NodeRecord] = []
    for ch in sorted(chunks, key=lambda c: int(c.get("ord", 0))):
        cid = str(ch["id"])
        body = str(ch.get("text") or "")
        out.append(
            NodeRecord(
                id=cid,
                type="CHUNK",
                doc_stem=stem,
                ord=int(ch.get("ord", 0)),
                text_preview=body[:240].replace("\n", " "),
            )
        )
    return out


def extract_all(chunks_dir: Path) -> list[NodeRecord]:
    nodes: list[NodeRecord] = []
    for path in load_chunk_files(chunks_dir):
        nodes.extend(nodes_from_chunk_file(path))
    return nodes
