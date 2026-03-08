import time
from typing import Callable

from fastapi import Request, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware


class RequestTimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        request.state.start_time = time.perf_counter()
        response = await call_next(request)
        return response


def init_middleware(app: FastAPI) -> None:
    app.add_middleware(RequestTimingMiddleware)
