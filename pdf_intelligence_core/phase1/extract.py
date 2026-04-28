"""Raw text extraction from PDF bytes."""

from __future__ import annotations

from io import BytesIO

from pypdf import PdfReader


def extract_text(content: bytes) -> list[str]:
    """One string per page (may be empty if page is image-only)."""
    reader = PdfReader(stream=BytesIO(content))
    return [page.extract_text() or "" for page in reader.pages]
