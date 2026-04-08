from fastapi import HTTPException

from dashboard.backend.auth import verify_password
from dashboard.backend.db import user_email_free, user_username_free

async def enforce_availability(email: str, username: str) -> None:
    if not await user_email_free(email):
        raise HTTPException(status_code=409, detail="Email is already in use.")
    
    if not await user_username_free(username):
        raise HTTPException(status_code=409, detail="Username is already in use.")

async def enforce_password_change_validity(current_password: str, current_password_hash: str, new_password: str, new_password_confirm: str) -> None:
    if not verify_password(stored_hash=current_password_hash, provided_password=current_password):
        raise HTTPException(status_code=401, detail="Your current password is incorrect.")
    
    if current_password == new_password:
        raise HTTPException(status_code=400, detail="New password must be different from the current password.")
    
    if new_password != new_password_confirm:
        raise HTTPException(status_code=400, detail="New passwords do not match.")