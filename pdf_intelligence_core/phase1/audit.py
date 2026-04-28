"""Lightweight structural audit of normalized text."""

from __future__ import annotations

from pdf_intelligence_core.types import AuditReport


def audit_normalized(page_texts: list[str], markdown: str) -> AuditReport:
    warnings: list[str] = []
    pages_with_text = sum(1 for p in page_texts if p and p.strip())
    if pages_with_text < len(page_texts):
        warnings.append("one or more pages have no extractable text (possible scan/OCR gap)")
    char_count = len(markdown)
    if char_count < 200:
        warnings.append("very short normalized output; downstream quality may suffer")
    return AuditReport(
        warnings=warnings,
        pages_with_text=pages_with_text,
        pages_total=len(page_texts),
        char_count=char_count,
    )
