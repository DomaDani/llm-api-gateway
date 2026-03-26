from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import os
from gateway.clients import UpstreamClient
from gateway.routes import chat_router, health_router
from gateway.app.middleware import init_middleware

from shared.config import TARGET_URL, TARGET_KEY

logger = logging.getLogger("uvicorn.error")

@asynccontextmanager
async def lifespan(app: FastAPI):
	await app.state.upstream_client.startup()
	yield
	await app.state.upstream_client.shutdown()

def create_app() -> FastAPI:
	app = FastAPI(title="LLM API Gateway", lifespan=lifespan)

	# Local CORS policy
	app.add_middleware(
		CORSMiddleware,
		allow_origins=["*"],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)

	url = os.getenv("TARGET_URL") or TARGET_URL
	key = os.getenv("TARGET_KEY") or TARGET_KEY

	logger.info(f"Initializing UpstreamClient with URL: {url}")
	app.state.upstream_client = UpstreamClient(url, key)

	init_middleware(app)

	app.include_router(chat_router)
	app.include_router(health_router)

	return app
