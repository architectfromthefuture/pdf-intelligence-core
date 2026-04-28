"""Phase 1: PDF validation with PyMuPDF."""

from pathlib import Path
import hashlib

import fitz


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_pdf(path: Path) -> dict:
    try:
        doc = fitz.open(path)
        pages = len(doc)

        if pages == 0:
            return {"valid": False, "error": "empty pdf"}

        return {
            "valid": True,
            "pages": pages,
            "hash": file_hash(path),
        }

    except Exception as error:
        return {
            "valid": False,
            "error": str(error),
        }
