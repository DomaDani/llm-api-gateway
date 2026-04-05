from fastapi import FastAPI

from shared.config import FRONTEND_ADDRESS

def init_middleware(app: FastAPI):
    # CORS middleware
    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"{FRONTEND_ADDRESS}:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)