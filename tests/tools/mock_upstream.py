#!/usr/bin/env python3

from __future__ import annotations
import argparse
import logging
from pathlib import Path
from typing import Dict, Any

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
        if "request" in data:
            if data["request"] == incoming:
                if data.get("completion") is not None:
                    return 200, data["completion"]
                elif data.get("upstream_error") is not None:
                    return data["upstream_error"]["status_code"], data["upstream_error"]["response"]
                break

    return 200, _mappings.get("mock_completion1")


@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    status_code, response = await _choose_mapping(request)    
    return JSONResponse(content=response, status_code=status_code)

@app.get("/health")
async def health():
    return JSONResponse(content={"status": "ok"}, status_code=200)


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
