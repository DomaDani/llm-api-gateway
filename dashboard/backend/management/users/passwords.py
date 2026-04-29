from fastapi import HTTPException

from shared.utils import verify_password

async def enforce_password_strength(password: str) -> None:
    """
    Validate password complexity requirements.
    A password is considered strong if it is at least 8 characters long and contains at least one uppercase letter, one lowercase letter, and one digit.

    Parameters
    ----------
    password : str
        Password value to validate.

    Returns
    -------
    None
        None.
    """
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long.")
    
    if not any(char.isupper() for char in password):
        raise HTTPException(status_code=400, detail="Password must contain at least one uppercase letter.")
    
    if not any(char.islower() for char in password):
        raise HTTPException(status_code=400, detail="Password must contain at least one lowercase letter.")
    
    if not any(char.isdigit() for char in password):
        raise HTTPException(status_code=400, detail="Password must contain at least one digit.")

async def enforce_password_change_validity(current_password: str, current_password_hash: str, new_password: str, new_password_confirm: str) -> None:
    """
    Validate a password change request for correctness and strength.

    Parameters
    ----------
    current_password : str
        Current plain-text password provided by the user.
    current_password_hash : str
        Stored password hash for the user.
    new_password : str
        Requested new plain-text password.
    new_password_confirm : str
        Confirmation of the new password.

    Returns
    -------
    None
        None.
    """
    if not verify_password(stored_hash=current_password_hash, provided_password=current_password):
        raise HTTPException(status_code=400, detail="Your current password is incorrect.")
    
    await enforce_password_strength(new_password)

    if current_password == new_password:
        raise HTTPException(status_code=400, detail="New password must be different from the current password.")
    
    if new_password != new_password_confirm:
        raise HTTPException(status_code=400, detail="New passwords do not match.")