"""Deterministic character windows over normalized Markdown."""

from __future__ import annotations

from pathlib import Path


def window_text(text: str, max_chars: int, overlap: int) -> list[str]:
    text = text.strip()
    if not text:
        return []
    if len(text) <= max_chars:
        return [text]
    stride = max(1, max_chars - overlap)
    out: list[str] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + max_chars)
        out.append(text[start:end])
        if end >= len(text):
            break
        start += stride
    return out


def chunk_markdown_file(md_path: Path, *, max_chars: int, overlap: int) -> dict:
    raw = md_path.read_text(encoding="utf-8")
    parts = window_text(raw, max_chars, overlap)
    stem = md_path.stem
    chunks = []
    for i, body in enumerate(parts):
        cid = f"{stem}:{i:05d}"
        chunks.append({"id": cid, "text": body, "ord": i, "source_md": str(md_path.name)})
    return {"stem": stem, "source_path": str(md_path), "chunks": chunks}
