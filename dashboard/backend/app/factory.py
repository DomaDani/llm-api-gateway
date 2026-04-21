
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from dashboard.backend.routes import (
    health_router,
    login_router,
    me_router,
    register_router,
    change_identity_router,
    change_password_router,
    everyone_router,
    delete_user_router,
    logs_info_router,
    keys_create_router,
    keys_delete_router,
    keys_info_router,
    projects_all_router,
    projects_info_router,
    users_info_router,
    quota_info_router,
    quota_create_router,
    quota_delete_router,
    quota_limit_types_router,
    quota_periods_router,
    projects_create_router,
    projects_add_user_router,
    projects_remove_user_router,
    projects_delete_router,
)

from .middleware import init_middleware


def _format_validation_error(exc: RequestValidationError) -> str:
    """Convert FastAPI validation errors to a compact readable message."""

    parts: list[str] = []
    for err in exc.errors():
        location = " -> ".join(str(value) for value in err.get("loc", []))
        message = err.get("msg", "Validation error")
        parts.append(f"{location}: {message}" if location else message)
    return "; ".join(parts) if parts else "Validation error"


async def request_validation_exception_handler(_, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": _format_validation_error(exc)},
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Defines the lifespan of the Fastapi application, handling startup and shutdown events.
    """
    try:
        yield
    finally:
        pass

def create_app() -> FastAPI:
    """
    Creates the FastAPI application instance, sets up the lifespan context, initializes middleware, and includes the API routers for health, authentication, user management, logs, keys, projects, and quotas.
    """
    app = FastAPI(title="LLM API Gateway Dashboard", lifespan=lifespan)
    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
    
    init_middleware(app)
    app.include_router(health_router)
    app.include_router(login_router)
    app.include_router(register_router)
    app.include_router(me_router)
    app.include_router(change_identity_router)
    app.include_router(change_password_router)
    app.include_router(everyone_router)
    app.include_router(delete_user_router)
    app.include_router(logs_info_router)
    app.include_router(keys_create_router)
    app.include_router(keys_delete_router)
    app.include_router(keys_info_router)
    app.include_router(projects_all_router)
    app.include_router(projects_info_router)
    app.include_router(users_info_router)
    app.include_router(quota_info_router)
    app.include_router(quota_create_router)
    app.include_router(quota_delete_router)
    app.include_router(quota_limit_types_router)
    app.include_router(quota_periods_router)
    app.include_router(projects_create_router)
    app.include_router(projects_add_user_router)
    app.include_router(projects_remove_user_router)
    app.include_router(projects_delete_router)

    return app