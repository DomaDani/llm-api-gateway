import math

from fastapi import Depends, HTTPException
from genai_prices import Usage

from gateway.models import ValidatedRequest, OpenAIRequest
from shared.models import APIKey
from gateway.auth import validate_api_key
from gateway.utils import get_token_count, calculate_cost
from gateway.db import db_limit_check_and_allocation

from shared.config import DEFAULT_MAX_COMPLETION_TOKENS, QUOTA_STRICTNESS, PROVIDER_ID

async def check_limits_costs(body: OpenAIRequest, key_info: APIKey = Depends(validate_api_key)) -> ValidatedRequest:
    # est_input_tokens = await run_in_threadpool(get_token_count, body.messages)
    est_input_tokens = get_token_count(body.messages)
    est_completion_tokens = int(math.ceil((body.max_completion_tokens or DEFAULT_MAX_COMPLETION_TOKENS) * QUOTA_STRICTNESS))
    estimated_total_tokens = est_input_tokens + est_completion_tokens

    estimated_cost = calculate_cost(
        usage=Usage(
            input_tokens=est_input_tokens,
            output_tokens=est_completion_tokens
        ),
        model_ref=body.model,
        provider_id=PROVIDER_ID
    )

    if not await db_limit_check_and_allocation(key_info, estimated_total_tokens, estimated_cost):
        raise HTTPException(status_code=429, detail="Quota exceeded.")
    


    return ValidatedRequest(
        key_id=key_info.id,
        project_id=key_info.project_id,
        user_id=key_info.user_id,
        body=body,
        estimated_tokens=estimated_total_tokens,
        internal_cost_estimate=estimated_cost
    )