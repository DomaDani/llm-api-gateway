import secrets
import hashlib
import hmac


# Utilities for hashing and verifying keys

def hash_key(api_key: str, salt: str = None) -> str:
    
    salt = secrets.token_bytes(16)

    hash_bytes = hashlib.pbkdf2_hmac(
        "sha256",
        api_key.encode("utf-8"),
        salt,
        iterations=1
    )

    return f"{salt.hex()}.{hash_bytes.hex()}"

def verify_key(key_attempt: str, hashed_key: str) -> bool:
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