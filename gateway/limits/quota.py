from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from gateway.models import ValidatedRequest, OpenAIRequest
from shared.models import APIKey
from gateway.auth import validate_api_key
from gateway.utils import get_token_count
from gateway.db import db_limit_check_and_allocation

from shared.config import DEFAULT_MAX_COMPLETION_TOKENS, QUOTA_STRICTNESS

async def check_limits_costs(body: OpenAIRequest, key_info: APIKey = Depends(validate_api_key)) -> ValidatedRequest:
    # est_input_tokens = await run_in_threadpool(get_token_count, body.messages)
    est_input_tokens = get_token_count(body.messages)


    est_completion_tokens = body.max_completion_tokens or DEFAULT_MAX_COMPLETION_TOKENS

    estimated_total_tokens = est_input_tokens + (est_completion_tokens * QUOTA_STRICTNESS)

    if not await db_limit_check_and_allocation(key_info, estimated_total_tokens):
        raise HTTPException(status_code=429, detail="Quota exceeded.")
    


    return ValidatedRequest(
        key_id=key_info.id,
        project_id=key_info.project_id,
        user_id=key_info.user_id,
        body=body,
        estimated_tokens=estimated_total_tokens,
        internal_cost=None # None for now, change later.
    )