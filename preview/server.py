"""Dev-only preview harness for greet-cli (sandbox only).

greet-cli is a command-line tool, so it has no web UI of its own. This module
exists only so the sandbox preview (host port 3000) can drive the real CLI from
a browser. It is not part of the published package: nothing in ``src/greet_cli``
imports it, and it never changes CLI behaviour.

Run it with:  uvicorn preview.server:app --host 0.0.0.0 --port 3000 --reload
"""

from __future__ import annotations

import contextlib
import io
import shlex
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from greet_cli import __version__
from greet_cli.cli import main as greet_main

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(title="greet-cli preview harness")


class GreetRequest(BaseModel):
    name: str = "world"
    times: int = Field(default=1, ge=1, le=50)
    shout: bool = False


def run_greet(name: str, times: int, shout: bool) -> tuple[int, list[str], list[str]]:
    """Invoke the real CLI entry point and capture what it prints."""
    argv = [name]
    if times != 1:
        argv += ["--times", str(times)]
    if shout:
        argv.append("--shout")

    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        try:
            exit_code = greet_main(argv)
        except SystemExit as exc:  # --version / argparse errors
            exit_code = int(exc.code or 0)

    lines = buffer.getvalue().splitlines()
    return exit_code, lines, ["greet", *argv]


def render_index() -> str:
    html = (STATIC_DIR / "index.html").read_text(encoding="utf-8")
    return html.replace("{{VERSION}}", __version__)


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return render_index()


@app.post("/api/greet")
def greet(payload: GreetRequest) -> dict:
    exit_code, lines, argv = run_greet(payload.name, payload.times, payload.shout)
    return {
        "command": " ".join(shlex.quote(part) for part in argv),
        "exit_code": exit_code,
        "lines": lines,
        "version": __version__,
    }
