# Docker runtime

`pdf-intelligence-core` can run inside Docker so the pipeline has a **reproducible execution environment** while keeping generated artifacts on the host machine.

The design is simple:

```text
Docker container = execution layer
./data           = persistent artifact layer
Python pipeline  = deterministic logic
```

## Why Docker matters

The pipeline depends on Python packages, PDF parsing libraries, embedding tools, and local filesystem paths. Docker keeps those layers stable:

- same Python version
- same system packages
- same Python dependencies (see `requirements.txt` / editable install)
- same CLI commands
- same mounted data layout (`./data:/app/data`)

That reduces machine-to-machine drift.

## Persistent data

Compose mounts `./data:/app/data`. Writes under `/app/data` appear on the host in `data/`. Stop or rebuild the container without deleting host artifacts—as long as you keep `./data`.

## Quick start

```bash
docker compose build
docker compose up -d
docker exec -it pdf_intelligence_core bash
python -m cli ingest
docker compose down
```

## Commands inside the container

Use the multiplexed CLI (same semantics as `pdf-core-*` on the host):

```bash
python -m cli ingest
python -m cli index
python -m cli query "what is this document about?"
python -m cli graph
```

Expectation when `data/inbox/` is empty:

```text
No PDFs found in data/inbox/
```

That still confirms ingestion ran inside the routed environment.

## Expected artifacts (abbreviated)

| Command | Typical outputs |
|--------|----------------|
| ingest | `data/markdown/*.md`, `data/audit/*.json` |
| index | `data/chunks/`, `data/embeddings/`, `data/vectors/`, `data/traces/` |
| query | JSON on stdout |
| graph | `data/graphs/nodes.json`, `edges.json`, `graph_index.json`, traces |

## Stop the container

```bash
docker compose down
```

## Operational modes

**Manual.** Start the container, `docker exec … bash`, run commands interactively — best while debugging.

**Semi-auto.** Keep the compose service up (`tail -f /dev/null`) and run whichever phase you need; data stays mounted.

**Full-auto (not v0.1).** A file watcher over `data/inbox/` is a later upgrade deliberately out of scope.

## Design boundary

**Inside Docker:** deterministic phases, reproducible environment, minimal host coupling.

**Outside Docker:** file housekeeping, notebooks, docs, publishing.

The container is the engine; `./data/` is durable memory between runs.
