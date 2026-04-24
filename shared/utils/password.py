from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError

ph = PasswordHasher()

def hash_password(password: str) -> str:
    """
    Hashes a plaintext password using Argon2 and returns the resulting hash string. The returned hash includes all necessary parameters and salt for later verification.

    Parameters
    ----------
    - password: The plaintext password to be hashed.
    """
    return ph.hash(password)

def verify_password(stored_hash: str, provided_password: str) -> bool:
    """
    Verifies a provided password against a stored hash using Argon2.

    Parameters
    ----------
    - stored_hash: The Argon2 hash string stored in the database, which includes the salt and parameters.
    - provided_password: The plaintext password attempt to verify against the stored hash.

    Returns
    -------
    - bool: True if the provided password is valid and matches the stored hash, False otherwise.
    """
    try:
        ph.verify(stored_hash, provided_password)
        return True
    except (VerifyMismatchError, InvalidHashError):
        return False