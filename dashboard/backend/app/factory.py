
from contextlib import asynccontextmanager
from fastapi import FastAPI

from dashboard.backend.routes import (
    health_router,
    login_router,
    me_router,
    register_router,
    change_identity_router,
    change_password_router,
    everyone_router,
    delete_user_router,
    projects_all_router,
    users_info_router,
    quota_info_router,
    projects_create_router,
    projects_add_user_router
)

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
    app.include_router(register_router)
    app.include_router(me_router)
    app.include_router(change_identity_router)
    app.include_router(change_password_router)
    app.include_router(everyone_router)
    app.include_router(delete_user_router)
    app.include_router(projects_all_router)
    app.include_router(users_info_router)
    app.include_router(quota_info_router)
    app.include_router(projects_create_router)
    app.include_router(projects_add_user_router)

    return app