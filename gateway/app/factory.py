from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from gateway.clients import UpstreamClient
from gateway.routes import chat_router, health_router
from gateway.app.middleware import init_middleware

from shared.config import TARGET_URL, TARGET_KEY

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

	app.state.upstream_client = UpstreamClient(TARGET_URL, TARGET_KEY)

	init_middleware(app)

	app.include_router(chat_router)
	app.include_router(health_router)

	return app
