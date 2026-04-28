"""Deterministic entity hints from plain chunk text (regex only)."""

from __future__ import annotations

import re


def extract_entities(chunk: str) -> dict:
    patterns = re.findall(
        r"\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)\b",
        chunk,
    )

    entities = sorted(set(patterns))

    return {
        "entities": entities,
        "method": "regex_capital_phrase",
    }
