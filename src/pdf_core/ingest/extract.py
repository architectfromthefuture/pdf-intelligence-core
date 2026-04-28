"""Phase 1: deterministic extraction with a plain-text fallback."""

from pathlib import Path

import pdfplumber
import pymupdf4llm


def extract_pymupdf(pdf_path: Path) -> str:
    return pymupdf4llm.to_markdown(str(pdf_path))


def extract_pdfplumber(pdf_path: Path) -> str:
    text: list[str] = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)

    return "\n\n".join(text)


def extract(pdf_path: Path) -> dict:
    try:
        return {
            "method": "pymupdf4llm",
            "text": extract_pymupdf(pdf_path),
        }
    except Exception as primary_error:
        body = extract_pdfplumber(pdf_path)
        return {
            "method": "pdfplumber",
            "text": body,
            "fallback_reason": str(primary_error),
        }
