"""Normalize page text to stable Markdown-oriented plain text."""

from __future__ import annotations

import re


def _collapse_ws(s: str) -> str:
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def normalize_to_markdown(page_texts: list[str]) -> str:
    """Join pages with headings; suitable as LLM-facing document text."""
    parts: list[str] = []
    for i, raw in enumerate(page_texts, start=1):
        body = _collapse_ws(raw)
        parts.append(f"## Page {i}\n\n{body if body else '_[no extractable text]_'}")
    return "\n\n".join(parts).strip() + "\n"
