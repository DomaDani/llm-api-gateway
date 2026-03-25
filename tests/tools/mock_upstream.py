#!/usr/bin/env python3

from __future__ import annotations
import argparse
import json
import logging
from pathlib import Path
from typing import Dict, Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager

log = logging.getLogger("mock_upstream")

_mappings = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Mock upstream starting; %d mappings available", len(_mappings))
    yield
    log.info("Mock upstream shutting down")


app = FastAPI(title="Mock Upstream", docs_url=None, redoc_url=None, lifespan=lifespan)


def load_mappings_from_dir(directory: Path) -> None:
    if not directory.exists():
        log.warning("Mappings directory %s does not exist", directory)
        return
    for p in sorted(directory.iterdir()):
        if p.is_file() and p.suffix.lower() == ".json":
            try:
                with p.open("r", encoding="utf-8") as fh:
                    data = json.load(fh)
                _mappings[p.stem] = data
                log.info("Loaded mapping %s from %s", p.stem, p)
            except Exception as e:
                log.exception("Failed loading mapping from %s: %s", p, e)


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Mock upstream starting; %d mappings available", len(_mappings))
    yield
    log.info("Mock upstream shutting down")


async def _choose_mapping(request: Request) -> Dict[str, Any]:
    incoming = await request.json()

    for _, data in _mappings.items():
        if "request" in data:
            if data["request"] == incoming:
                if "completion" in data:
                    return data["completion"]
                break

    return _mappings.get("mock_completion1")


@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    mapping = await _choose_mapping(request)
    return JSONResponse(content=mapping, status_code=200)


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=8081)
    p.add_argument("--host", default="0.0.0.0")
    p.add_argument("--mappings", default="tests/fixtures/llm_responses/completions")
    p.add_argument("--reload", action="store_true", default=False)
    args = p.parse_args(argv)

    logging.basicConfig(level=logging.INFO)

    mappings_dir = Path(args.mappings)
    load_mappings_from_dir(mappings_dir)

    uvicorn.run(app, host=args.host, port=args.port, log_level="info", reload=args.reload)


if __name__ == "__main__":
    main()
