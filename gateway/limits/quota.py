from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ..models.pydantic.quotas import KeyInfo, ValidatedRequest
from ..models.pydantic.openai import OpenAIRequest
from ..auth.keys import validate_api_key
from ..utils.usage import get_token_count
from ..db.mock_db import mock_limit_change

from ..config import DEFAULT_MAX_COMPLETION_TOKENS, QUOTA_STRICTNESS

async def check_limits_costs(body: OpenAIRequest, key_info: KeyInfo = Depends(validate_api_key)) -> ValidatedRequest:
    # est_input_tokens = await run_in_threadpool(get_token_count, body.messages)
    est_input_tokens = get_token_count(body.messages)


    est_completion_tokens = body.max_completion_tokens or DEFAULT_MAX_COMPLETION_TOKENS

    estimated_total_tokens = est_input_tokens + (est_completion_tokens * QUOTA_STRICTNESS)

    remaining_tokens = key_info.limit_value - key_info.spent_value

    if estimated_total_tokens > remaining_tokens:
        raise HTTPException(status_code=429, detail="Quota exceeded.")
    
    mock_limit_change(key_info.id, estimated_total_tokens)

    return ValidatedRequest(
        body=body,
        estimated_tokens=estimated_total_tokens,
        key_id=key_info.id
    )