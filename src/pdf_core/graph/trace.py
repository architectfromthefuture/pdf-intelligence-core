"""Phase 3 traces (chunk-level extraction provenance)."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from pdf_core.config import repo_root


def traces_dir() -> Path:
    return repo_root() / "data/graphs/traces"


def write_trace(name: str, payload: dict) -> Path:
    td = traces_dir()
    td.mkdir(parents=True, exist_ok=True)

    body = dict(payload)
    body["timestamp"] = datetime.now(UTC).isoformat()

    out = td / f"{name}.json"
    out.write_text(json.dumps(body, indent=2), encoding="utf-8")

    return out