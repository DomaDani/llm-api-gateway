from contextlib import asynccontextmanager
import logging
from pathlib import Path
import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from genai_prices import UpdatePrices, data as data_module, data_snapshot
from genai_prices.data_snapshot import DataSnapshot

from gateway.clients import UpstreamClient
from gateway.routes import chat_router, health_router
from gateway.app.middleware import init_middleware
from gateway.db.refresh import refresh_quotas_by_batch
from gateway.db.helpers import get_quota_count

from shared.config import TARGET_URL, TARGET_KEY
from shared.utils import find_project_root

logger = logging.getLogger("uvicorn.error")

@asynccontextmanager
async def lifespan(app: FastAPI):
	await app.state.upstream_client.startup()
	app.state.reset_task = asyncio.create_task(_quota_refresh_job())
	app.state.price_update_task = asyncio.create_task(_price_update_job())
	try:
		yield
	finally:
		app.state.reset_task.cancel()
		app.state.price_update_task.cancel()
		try:
			await app.state.reset_task
			await app.state.price_update_task
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

async def _quota_refresh_job():
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

async def _price_update_job():
	while True:
		try:
			with UpdatePrices() as updater:
				updater.wait()
				_merge_custom_providers()
				logger.info("Price update completed.")
		except Exception:
			logger.exception("Price update failed")
		await asyncio.sleep(3600)

def _merge_custom_providers():
	providers_file = find_project_root() / "shared/config/providers.json"

	if providers_file.exists():
		raw = providers_file.read_bytes()
		
		try:
			custom_providers = data_module.providers_schema.validate_json(raw)
			merged = list(data_module.providers)[:]
			existing_ids = {p.id for p in merged}
			for provider in custom_providers:
				if provider.id in existing_ids:
					orig_id = provider.id
					i = 1
					while f"{orig_id}_{i}" in existing_ids:
						i += 1
					provider.id = f"{orig_id}_{i}"
				merged.append(provider)
				existing_ids.add(provider.id)

			data_snapshot.set_custom_snapshot(DataSnapshot(providers=merged, from_auto_update=False))
		except Exception as e:
			logger.error(f"Failed to load custom providers from {providers_file}: {e}")
	else:
		logger.info(f"No custom providers file found at {providers_file}, using bundled providers.")