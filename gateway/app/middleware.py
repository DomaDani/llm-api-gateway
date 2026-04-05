import time
from typing import Callable

from fastapi import Request, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware


class RequestTimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        request.state.start_time = time.perf_counter()
        response = await call_next(request)
        return response


def init_middleware(app: FastAPI) -> None:

    app.add_middleware(RequestTimingMiddleware)
    app.add_middleware(
		CORSMiddleware,
		allow_origins=["*"],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)
