from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from gateway.utils import verify_key
from gateway.db import db_key_check
from shared.models import APIKey

from shared.config import EXPECTED_KEY_LENGTH
from shared.models import Status

# Key validation module

security = HTTPBearer()

async def validate_api_key(auth: HTTPAuthorizationCredentials = Security(security)) -> APIKey:
    api_key = auth.credentials

    if not api_key:
        raise HTTPException(status_code=401, detail="Missing API Key from headers.")
    if len(api_key) < EXPECTED_KEY_LENGTH:
        raise HTTPException(status_code=400, detail="Invalid API Key length.")
    
    try:
        key_data = await db_key_check(api_key)
    except ValueError:
        raise HTTPException(status_code=401, detail="API key fingerprint not in allowed keys.")
    
    if key_data.status != Status.ACTIVE:
        raise HTTPException(status_code=403, detail="The API key is not active.")
    
    # is_valid = await run_in_threadpool(verify_key, api_key, key_data["key_hash"])
    is_valid = verify_key(api_key, key_data.key_hash)

    if not is_valid:
        raise HTTPException(status_code=401, detail="Invalid API key.")

    return key_data