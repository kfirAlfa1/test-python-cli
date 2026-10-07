# AGENTS.md

## What this project is

`greet-cli` is a pure-stdlib Python command-line package (no runtime
dependencies, no web server). The whole app is `src/greet_cli/cli.py`, exposed
as the `greet` console script via `pyproject.toml` (`[project.scripts]`).

## Running it in this sandbox

```sh
docker compose -f docker-compose.base44.yml up -d --build
```

One service, `greet-preview`, runs `python:3.12-slim` with the repo bind-mounted
at `/app`:

1. installs the package in editable mode (`pip install -e .`) plus the
   preview-only harness deps from `preview/requirements.txt`,
2. serves `preview/server.py` with `uvicorn --reload` on `0.0.0.0:3000`.

Edits under `src/` or `preview/` are picked up by the reload watcher (a page
refresh is enough for HTML/CSS changes).

## The preview harness (not part of the package)

`preview/` is a sandbox-only shim, because a CLI has no UI to preview: the
browser page takes name / `--times` / `--shout`, calls the **real**
`greet_cli.cli.main()` in-process, and prints its captured output. Nothing in
`src/greet_cli` imports `preview/`, and the harness does not alter CLI
behaviour — keep it that way.

`fastapi` / `uvicorn` (see `preview/requirements.txt`) are preview-only and are
deliberately not listed in `pyproject.toml`.

## Verification

- `docker compose -f docker-compose.base44.yml ps` — service should be `healthy`.
- `curl -s localhost:3000/ | grep -q greet-cli` — the page is served.
- `docker compose -f docker-compose.base44.yml exec -T greet-preview greet Alice --times 2 --shout`
  — exercises the CLI itself.

There are no tests, migrations, seeds or external services, so no secrets are
required.
