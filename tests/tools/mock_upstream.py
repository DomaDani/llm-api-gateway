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
    """
    Manage startup and shutdown lifecycle logging for the mock upstream app.

    Parameters
    ----------
    app : FastAPI
        The FastAPI application instance.

    Returns
    -------
    Async context manager
        An async context manager controlling app lifespan events.
    """
    log.info(f"Mock upstream starting; {len(_mappings)} mappings available")
    yield
    log.info("Mock upstream shutting down")


app = FastAPI(title="Mock Upstream", docs_url=None, redoc_url=None, lifespan=lifespan)


async def _choose_mapping(request: Request) -> Dict[str, Any]:
    """
    Select the configured response mapping that matches an incoming request.

    Parameters
    ----------
    request : Request
        Incoming FastAPI request containing chat-completion JSON payload.

    Returns
    -------
    tuple[int, dict]
        A tuple of HTTP status code and response payload dictionary.
    """
    incoming = await request.json()

    for _, data in _mappings.items():
        if "request" in data and _matches(data["request"], incoming):
            if data.get("completion") is not None:
                return 200, data["completion"]

            ue = data.get("upstream_error")
            if ue is not None:
                status = int(ue.get("status") or 500)
                response = ue.get("response") or {"detail": "upstream error"}
                if not (isinstance(response, dict) and "error" in response):
                    message = response.get("detail") if isinstance(response, dict) else str(response)
                    response = {
                        "error": {
                            "message": message,
                            "type": "upstream_error",
                            "param": None,
                            "code": status,
                        }
                    }
                return status, response

            break

    # fallback to a known completion mapping if available
    fallback = _mappings.get("mock_completion1", {})
    if isinstance(fallback, dict) and fallback.get("completion") is not None:
        return 200, fallback["completion"]

    return 200, {"detail": "no mapping found"}

def _matches(expected, actual):
    """
    Recursively compare nested mapping structures for partial request matching.

    Parameters
    ----------
    expected : Any
        Expected structure from mapping fixture.
    actual : Any
        Actual value from incoming request payload.

    Returns
    -------
    bool
        True if the actual payload satisfies the expected structure, else False.
    """
    if isinstance(expected, dict) and isinstance(actual, dict):
        for k, v in expected.items():
            if k not in actual:
                return False
            if not _matches(v, actual[k]):
                return False
        return True
    if isinstance(expected, list) and isinstance(actual, list):
        if len(expected) != len(actual):
            return False
        for e_item, a_item in zip(expected, actual):
            if not _matches(e_item, a_item):
                return False
        return True
    return expected == actual

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    """
    Handle chat completion requests using mapping-driven mocked responses.

    Parameters
    ----------
    request : Request
        Incoming FastAPI request.

    Returns
    -------
    JSONResponse
        A JSONResponse containing mocked completion or upstream-error payload.
    """
    status, response = await _choose_mapping(request)
    if status == 200:
        response = dict(response)
        response["id"] += str(randint(1000, 999999))
    return JSONResponse(content=response, status_code=status)

@app.get("/health")
async def health():
    """Return a simple health-check response for test orchestration."""

    return JSONResponse(content={"status": "ok"}, status_code=200)


def main(argv=None):
    """
    Start the mock upstream server with mappings loaded from fixture files.

    Parameters
    ----------
    argv : list[str] | None
        Optional CLI argument list.

    Returns
    -------
    None
        None.
    """
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
