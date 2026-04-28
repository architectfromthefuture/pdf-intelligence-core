"""Chunk normalized Markdown into retrieval units."""

from __future__ import annotations

import re
import uuid

from pdf_intelligence_core.types import Chunk


_PAGE_HDR = re.compile(r"^## Page (\d+)\s*$")


def _estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def _windows(text: str, *, max_chars: int, overlap_chars: int) -> list[str]:
    text = text.strip()
    if not text:
        return []
    if len(text) <= max_chars:
        return [text]
    stride = max(1, max_chars - overlap_chars)
    out: list[str] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + max_chars)
        out.append(text[start:end])
        if end >= len(text):
            break
        start += stride
    return out


def chunk_markdown(
    markdown: str,
    *,
    max_chars: int = 1200,
    overlap_chars: int = 100,
) -> list[Chunk]:
    """Split on ``## Page N`` headings, then sliding windows inside each page."""
    sections: list[tuple[int, str]] = []
    current_page = 1
    buf: list[str] = []
    saw_header = False

    for line in markdown.splitlines():
        m = _PAGE_HDR.match(line.strip())
        if m:
            if buf:
                sections.append((current_page, "\n".join(buf)))
                buf = []
            current_page = int(m.group(1))
            saw_header = True
        else:
            buf.append(line)

    if buf or not saw_header:
        body = "\n".join(buf) if buf else markdown
        sections.append((current_page, body.strip()))

    chunks: list[Chunk] = []
    for page_no, body in sections:
        body = body.strip()
        windows = _windows(body, max_chars=max_chars, overlap_chars=overlap_chars)
        if not windows:
            continue
        for w in windows:
            cid = f"c_{uuid.uuid4().hex[:12]}"
            chunks.append(
                Chunk(
                    id=cid,
                    text=w,
                    page_start=page_no,
                    page_end=page_no,
                    token_estimate=_estimate_tokens(w),
                )
            )

    return chunks or [
        Chunk(
            id=f"c_{uuid.uuid4().hex[:12]}",
            text="",
            page_start=1,
            page_end=1,
            token_estimate=1,
        )
    ]
