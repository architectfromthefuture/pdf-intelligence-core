"""Run-level trace records for Phase 2."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def write_trace(payload: dict[str, Any], directory: Path, name: str) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    body = dict(payload)
    body["timestamp"] = datetime.now(UTC).isoformat()
    out = directory / f"{name}.json"
    out.write_text(json.dumps(body, indent=2), encoding="utf-8")
    return out
