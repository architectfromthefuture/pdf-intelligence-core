"""Persist audit trails as JSON."""

import json
from datetime import UTC, datetime
from pathlib import Path


def write_audit(record: dict, directory: Path, filename: str) -> Path:
    directory.mkdir(parents=True, exist_ok=True)

    record = dict(record)
    record["timestamp"] = datetime.now(UTC).isoformat()

    out = directory / f"{filename}.json"
    out.write_text(json.dumps(record, indent=2), encoding="utf-8")

    return out
