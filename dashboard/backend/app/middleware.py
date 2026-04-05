from fastapi import FastAPI

from shared.config import FRONTEND_DOMAIN_ADDRESS

def init_middleware(app: FastAPI):
    # CORS middleware
    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_DOMAIN_ADDRESS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)