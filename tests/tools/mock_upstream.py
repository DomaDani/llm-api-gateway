#!/usr/bin/env python3

from __future__ import annotations
import argparse
import logging
from pathlib import Path
from typing import Dict, Any
from random import randint

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager
from tests.tools import load_mappings_from_dir

log = logging.getLogger("mock_upstream")

_mappings = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info(f"Mock upstream starting; {len(_mappings)} mappings available")
    yield
    log.info("Mock upstream shutting down")


app = FastAPI(title="Mock Upstream", docs_url=None, redoc_url=None, lifespan=lifespan)


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info(f"Mock upstream starting; {len(_mappings)} mappings available")
    yield
    log.info("Mock upstream shutting down")


async def _choose_mapping(request: Request) -> Dict[str, Any]:
    incoming = await request.json()

    for _, data in _mappings.items():
        if "request" in data and data["request"] == incoming:
            if data.get("completion") is not None:
                return 200, data["completion"]

            ue = data.get("upstream_error")
            if ue is not None:
                status = ue.get("status") or 500
                response = ue.get("response") or {"detail": "upstream error"}
                return int(status), response

            break

    # fallback to a known completion mapping if available
    fallback = _mappings.get("mock_completion1", {})
    if isinstance(fallback, dict) and fallback.get("completion") is not None:
        return 200, fallback["completion"]

    return 200, {"detail": "no mapping found"}


@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    status, response = await _choose_mapping(request)
    if status == 200:
        response["id"] += str(randint(1000, 999999))
    return JSONResponse(content=response, status_code=status)

@app.get("/health")
async def health():
    return JSONResponse(content={"status": "ok"}, status=200)


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=8081)
    p.add_argument("--host", default="0.0.0.0")
    p.add_argument("--mappings", default="tests/fixtures/completions")
    p.add_argument("--reload", action="store_true", default=False)
    args = p.parse_args(argv)

    logging.basicConfig(level=logging.INFO)

    mappings_dir = Path(args.mappings)
    _mappings.update(load_mappings_from_dir(mappings_dir))

    uvicorn.run(app, host=args.host, port=args.port, log_level="info", reload=args.reload)


if __name__ == "__main__":
    main()
