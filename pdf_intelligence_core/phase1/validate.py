"""PDF validation (magic bytes + parseability)."""

from __future__ import annotations

from io import BytesIO

PDF_MAGIC = b"%PDF"


def validate_pdf(content: bytes) -> tuple[bool, str]:
    """Return (ok, message). Does not imply text quality or OCR availability."""
    if not content.startswith(PDF_MAGIC):
        return False, "missing PDF header"
    try:
        from pypdf import PdfReader

        reader = PdfReader(stream=BytesIO(content))
        n = len(reader.pages)
        if n < 1:
            return False, "no pages"
    except Exception as exc:
        return False, f"unreadable PDF: {exc}"
    return True, "ok"
