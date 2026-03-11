from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from gateway.utils import verify_key
from gateway.db import mock_db_key_check, mock_db_limit_check
from gateway.models import KeyInfo

from llm_api_gateway_config.config import EXPECTED_KEY_LENGTH

# Key validation module

security = HTTPBearer()

async def validate_api_key(auth: HTTPAuthorizationCredentials = Security(security)) -> KeyInfo:
    api_key = auth.credentials

    if not api_key:
        raise HTTPException(status_code=401, detail="Missing API Key from headers.")
    if len(api_key) < EXPECTED_KEY_LENGTH:
        raise HTTPException(status_code=400, detail="Invalid API Key length.")
    
    key_data = mock_db_key_check(api_key)

    if not key_data:
        raise HTTPException(status_code=401, detail="API key fingerprint not in allowed keys.")
    
    if not key_data["is_active"]:
        raise HTTPException(status_code=403, detail="The API key is disabled.")
    
    # is_valid = await run_in_threadpool(verify_key, api_key, key_data["key_hash"])
    is_valid = verify_key(api_key, key_data["key_hash"])

    if not is_valid:
        raise HTTPException(status_code=401, detail="Invalid API key.")

    limit_data = mock_db_limit_check(key_data["id"])

    return KeyInfo(
        id=key_data["id"],
        limit_value=limit_data["limit_value"],
        spent_value=limit_data["spent_value"]
    )