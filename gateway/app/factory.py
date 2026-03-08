import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..clients.upstream import UpstreamClient
from ..routes.chat import router as chat_router
from ..routes.health import router as health_router
from .middleware import init_middleware

load_dotenv()

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

	upstream_base = os.getenv("TARGET_URL")
	upstream_key = os.getenv("TARGET_KEY")
	app.state.upstream_client = UpstreamClient(upstream_base, upstream_key)

	init_middleware(app)

	app.include_router(chat_router)
	app.include_router(health_router)

	return app
