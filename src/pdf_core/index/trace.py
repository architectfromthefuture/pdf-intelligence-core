"""Trace artifacts for every Phase 2 transformation."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from pdf_core.config import repo_root


TRACE_DIR = repo_root() / "data/traces"


def write_trace(name: str, payload: dict) -> Path:
    TRACE_DIR.mkdir(parents=True, exist_ok=True)

    body = dict(payload)
    body["timestamp"] = datetime.now(timezone.utc).isoformat()

    out = TRACE_DIR / f"{name}.json"
    out.write_text(json.dumps(body, indent=2), encoding="utf-8")

    return out
