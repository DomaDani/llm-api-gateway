import secrets
import hashlib
import hmac


# Utilities for hashing and verifying keys

def hash_key(api_key: str, salt: str = None) -> str:
    """
    Hashes the provided API key using PBKDF2 HMAC with SHA-256. It generates a random salt if one is not provided, and returns a string containing the salt and the hash separated by a period.

    Parameters
    ----------
    - api_key: The API key to be hashed.
    - salt: An optional salt value to use for hashing. If not provided, a random 16-byte salt will be generated.

    Returns
    -------
    - str: A string containing the hexadecimal representation of the salt and the hash, separated by a period.
    """
    
    salt = secrets.token_bytes(16)

    hash_bytes = hashlib.pbkdf2_hmac(
        "sha256",
        api_key.encode("utf-8"),
        salt,
        iterations=1
    )

    return f"{salt.hex()}.{hash_bytes.hex()}"

def verify_key(key_attempt: str, hashed_key: str) -> bool:
    """
    Verifies a key attempt against a stored hashed key hashed using the hash_key function. It extracts the salt and original hash from the stored hashed key, re-hashes the key attempt using the same salt, and compares the new hash with the original hash using a secure comparison method.

    Parameters
    ----------
    - key_attempt: The API key attempt to verify.
    - hashed_key: The stored hashed key string containing the salt and hash separated by a period.

    Returns
    -------
    - bool: True if the key attempt is valid and matches the stored hash, False otherwise.
    """
    try:
        salt_hex, og_hash_hex = hashed_key.split('.')
        salt = bytes.fromhex(salt_hex)
        og_hash = bytes.fromhex(og_hash_hex)
        
        new_hash = hashlib.pbkdf2_hmac(
            "sha256",
            key_attempt.encode("utf-8"),
            salt,
            iterations=1
        )

        return hmac.compare_digest(new_hash, og_hash)
    except Exception:
        return False