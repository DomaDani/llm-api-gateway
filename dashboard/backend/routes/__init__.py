from .users import me_router, change_identity_router, change_password_router, everyone_router, info_router
from .health import router as health_router
from .auth import login_router, register_router
from .projects import all_router

__all__ = [
    "health_router",
    "login_router",
    "register_router",
    "me_router",
    "change_identity_router",
    "change_password_router",
    "everyone_router",
    "all_router",
    "info_router"
]