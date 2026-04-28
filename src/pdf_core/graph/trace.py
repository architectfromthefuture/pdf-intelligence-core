"""Graph build traces."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def write_graph_trace(payload: dict[str, Any], traces_dir: Path, name: str = "graph_last") -> Path:
    traces_dir.mkdir(parents=True, exist_ok=True)
    body = dict(payload)
    body["timestamp"] = datetime.now(UTC).isoformat()
    out = traces_dir / f"{name}.json"
    out.write_text(json.dumps(body, indent=2), encoding="utf-8")
    return out
