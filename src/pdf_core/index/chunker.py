"""Deterministic fixed word-window chunking (stable chunk_id per window)."""

from __future__ import annotations

from typing import Any


def chunk_text(text: str, chunk_size: int = 500) -> dict[str, Any]:
    words = text.split()

    chunks: list[dict[str, Any]] = []

    for index, start in enumerate(range(0, len(words), chunk_size)):
        chunk_words = words[start : start + chunk_size]
        chunks.append(
            {
                "chunk_id": f"chunk_{index:04d}",
                "text": " ".join(chunk_words),
                "start_word": start,
                "end_word": start + len(chunk_words),
            }
        )

    return {
        "chunks": chunks,
        "chunk_size": chunk_size,
        "total_chunks": len(chunks),
        "strategy": "fixed_word_window",
    }
