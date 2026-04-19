import time
from typing import Callable

from fastapi import Request, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware


class RequestTimingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to measure the time taken by the gateway to process each request.
    """
    async def dispatch(self, request: Request, call_next: Callable):
        """
        Records the start time of the request processing, calls the next middleware or route handler, and then returns the response.

        Parameters
        ----------
        - request: The incoming FastAPI Request object.
        - call_next: A callable that takes a Request and returns a Response, representing the next step in the middleware chain or the final route handler.
        """
        request.state.start_time = time.perf_counter()
        response = await call_next(request)
        return response


def init_middleware(app: FastAPI) -> None:
    """
    Initializes the middleware for the FastAPI application, including the RequestTimingMiddleware for measuring request processing time and the CORSMiddleware for handling Cross-Origin Resource Sharing (CORS) with permissive settings.
    """

    app.add_middleware(RequestTimingMiddleware)
    app.add_middleware(
		CORSMiddleware,
		allow_origins=["*"],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)
