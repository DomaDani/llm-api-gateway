
from contextlib import asynccontextmanager
from fastapi import FastAPI

from backend.routes import health_router, login_router, me_router

from .middleware import init_middleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        pass

def create_app() -> FastAPI:
    app = FastAPI(title="LLM API Gateway Dashboard", lifespan=lifespan)
    
    init_middleware(app)
    app.include_router(health_router)
    app.include_router(login_router)
    app.include_router(me_router)

    return app