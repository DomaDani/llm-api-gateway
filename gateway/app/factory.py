from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from gateway.clients import UpstreamClient
from gateway.routes import chat_router, health_router
from gateway.app.middleware import init_middleware
from gateway.db.refresh import refresh_quotas_by_batch
from gateway.db.helpers import get_quota_count

from shared.config import TARGET_URL, TARGET_KEY

logger = logging.getLogger("uvicorn.error")

@asynccontextmanager
async def lifespan(app: FastAPI):
	await app.state.upstream_client.startup()
	app.state.reset_task = asyncio.create_task(_reset_loop())
	try:
		yield
	finally:
		app.state.reset_task.cancel()
		try:
			await app.state.reset_task
		except asyncio.CancelledError:
			pass
		await app.state.upstream_client.shutdown()

def create_app() -> FastAPI:
	app = FastAPI(title="LLM API Gateway", lifespan=lifespan)

	app.add_middleware(
		CORSMiddleware,
		allow_origins=["*"],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)

	logger.info("TARGET_URL=%s", TARGET_URL)
	app.state.upstream_client = UpstreamClient(TARGET_URL, TARGET_KEY)

	init_middleware(app)
	app.include_router(chat_router)
	app.include_router(health_router)

	return app

async def _reset_loop():
	while True:
		try:
			total_count = await get_quota_count()
			change_count = 0
			for _ in range(0, total_count // 100 + 1):
				change_count += await refresh_quotas_by_batch(batch_size=100)
				if change_count == 0:
					break
			logger.info(f"Quota reset completed: {change_count} quotas reset")

		except Exception:
			logger.exception("quota reset failed")
		await asyncio.sleep(60)