"""Multiplex `python -m cli <command>` alongside console-script entrypoints."""

from __future__ import annotations

import argparse
import sys

from cli.graph import main as graph_main
from cli.ingest import main as ingest_main
from cli.index import main as index_main
from cli.query import main as query_main


def main(argv: list[str] | None = None) -> None:
    argv = list(sys.argv[1:] if argv is None else argv)

    parser = argparse.ArgumentParser(
        prog="python -m cli",
        description=(
            "Run pdf-intelligence-core pipeline phases (same behavior as pdf-core-* scripts)."
        )
    )
    parser.add_argument(
        "command",
        choices=["ingest", "index", "graph", "query"],
        nargs="?",
        help="Pipeline command.",
    )

    parsed, remaining = parser.parse_known_args(argv)

    if parsed.command is None:
        parser.print_help()
        sys.exit(0)

    if parsed.command == "ingest":
        ingest_main()
    elif parsed.command == "index":
        index_main()
    elif parsed.command == "graph":
        graph_main()
    elif parsed.command == "query":
        if not remaining:
            print(
                "usage: python -m cli query [-k N] QUERY",
                file=sys.stderr,
            )
            sys.exit(2)
        query_main(remaining)


if __name__ == "__main__":
    main()
