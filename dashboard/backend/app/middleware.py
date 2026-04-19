from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from shared.config import FRONTEND_ADDRESS

def init_middleware(app: FastAPI):
    """
    Initializes the middleware for the FastAPI application, including the CORSMiddleware for handling Cross-Origin Resource Sharing (CORS) with permissive settings.
    """
    app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"{FRONTEND_ADDRESS}:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)