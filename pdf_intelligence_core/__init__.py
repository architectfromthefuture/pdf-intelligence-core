"""pdf-intelligence-core: phased PDF → retrieval → graph pipeline."""

from pdf_intelligence_core.pipeline import PipelineConfig, PipelineResult, run_pipeline
from pdf_intelligence_core.types import (
    ArtifactRef,
    AuditReport,
    Chunk,
    DocumentGraph,
    GraphEdge,
    GraphNode,
    IndexRecord,
)

__all__ = [
    "ArtifactRef",
    "AuditReport",
    "Chunk",
    "DocumentGraph",
    "GraphEdge",
    "GraphNode",
    "IndexRecord",
    "PipelineConfig",
    "PipelineResult",
    "run_pipeline",
]

__version__ = "0.1.0"
