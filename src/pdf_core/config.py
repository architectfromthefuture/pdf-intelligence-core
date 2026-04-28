"""Load `configs/settings.yaml` and resolve repo-root paths."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

_REPO_ROOT = Path(__file__).resolve().parents[2]


def repo_root() -> Path:
    return _REPO_ROOT


@dataclass(frozen=True)
class Settings:
    inbox: Path
    markdown: Path
    audit: Path
    chunks: Path
    embeddings: Path
    vectors: Path
    traces: Path
    graphs: Path
    graph_traces: Path
    chunk_max_chars: int
    chunk_overlap_chars: int
    embedding_dim: int
    embedding_normalize: bool
    retrieve_top_k: int


def load_settings(path: Path | None = None) -> Settings:
    cfg_path = path or (_REPO_ROOT / "configs" / "settings.yaml")
    data = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
    p = data["paths"]
    c = data["chunk"]
    e = data["embedding"]
    r = data["retrieve"]
    return Settings(
        inbox=_REPO_ROOT / p["inbox"],
        markdown=_REPO_ROOT / p["markdown"],
        audit=_REPO_ROOT / p["audit"],
        chunks=_REPO_ROOT / p["chunks"],
        embeddings=_REPO_ROOT / p["embeddings"],
        vectors=_REPO_ROOT / p["vectors"],
        traces=_REPO_ROOT / p["traces"],
        graphs=_REPO_ROOT / p["graphs"],
        graph_traces=_REPO_ROOT / p["graph_traces"],
        chunk_max_chars=int(c["max_chars"]),
        chunk_overlap_chars=int(c["overlap_chars"]),
        embedding_dim=int(e["dim"]),
        embedding_normalize=bool(e["normalize"]),
        retrieve_top_k=int(r["top_k"]),
    )
