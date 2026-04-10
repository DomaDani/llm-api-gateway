from .users import me_router, change_identity_router, change_password_router, everyone_router, users_info_router, delete_user_router
from .health import router as health_router
from .auth import login_router, register_router
from .projects import projects_all_router, projects_create_router, projects_add_user_router, projects_delete_router
from .quotas import quota_info_router

__all__ = [
    "health_router",
    "login_router",
    "register_router",
    "me_router",
    "change_identity_router",
    "change_password_router",
    "everyone_router",
    "delete_user_router",
    "projects_all_router",
    "projects_add_user_router",
    "projects_delete_router",
    "users_info_router",
    "quota_info_router",
    "projects_create_router"
]