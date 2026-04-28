"""Optional CLI demo."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from pdf_intelligence_core.pipeline import PipelineConfig, run_pipeline


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run pdf-intelligence-core pipeline")
    parser.add_argument("pdf", type=str, help="Path to PDF file, or - for stdin")
    parser.add_argument(
        "--query",
        "-q",
        default="summarize main topics",
        help="Retrieval probe string",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON summary instead of prose",
    )
    args = parser.parse_args(argv)

    raw = sys.stdin.buffer.read() if args.pdf == "-" else Path(args.pdf).read_bytes()
    cfg = PipelineConfig()
    result = run_pipeline(raw, query=args.query, config=cfg)

    if args.json:
        out = {
            "validation_message": result.validation_message,
            "audit": {
                "warnings": result.audit.warnings,
                "pages_with_text": result.audit.pages_with_text,
                "pages_total": result.audit.pages_total,
                "char_count": result.audit.char_count,
            },
            "chunks": len(result.chunks),
            "graph_nodes": len(result.graph.nodes),
            "graph_edges": len(result.graph.edges),
            "top_retrieval_scores": [
                {"score": s, "chunk_id": rec.chunk_id, "preview": rec.text[:200]}
                for s, rec in result.retrieval_sample
            ],
        }
        json.dump(out, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0

    sys.stdout.write(f"validation: {result.validation_message}\n")
    sys.stdout.write(
        f"audit: warnings={len(result.audit.warnings)}, "
        f"pages_with_text={result.audit.pages_with_text}/{result.audit.pages_total}\n"
    )
    sys.stdout.write(f"chunks={len(result.chunks)} graph_nodes={len(result.graph.nodes)}\n")
    sys.stdout.write("top retrieval hits:\n")
    for score, rec in result.retrieval_sample:
        snippet = rec.text.replace("\n", " ")[:120]
        sys.stdout.write(f"  [{score:.3f}] {rec.chunk_id} — {snippet}…\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
