from .all import router as projects_all_router
from .info import router as projects_info_router
from .create import router as projects_create_router
from .add_user import router as projects_add_user_router
from .remove_user import router as projects_remove_user_router
from .delete import router as projects_delete_router

__all__ = ["projects_all_router", "projects_info_router", "projects_create_router", "projects_add_user_router", "projects_remove_user_router", "projects_delete_router"]