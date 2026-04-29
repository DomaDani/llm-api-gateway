from datetime import datetime, timezone
from fastapi import Request
from genai_prices import Usage

from gateway.models import ValidatedRequest, UsageLogEntry
from gateway.logging import usage_logger
from gateway.utils import calculate_cost

from shared.config import PROVIDER_ID

async def prepare_usage_entry(
    request: Request,
    validated_request: ValidatedRequest,
    upstream_latency,
    gateway_overhead,
    ttft,
    total_time,
    chat_completion=None, 
    status_code=200,
    failed_upstream=False
):
    """
    Extract the relevant usage information from the completion response and calls the logger to store it in the database.

    Parameters
    ----------
    request : Request
        The original FastAPI request object.
    validated_request : ValidatedRequest
        The validated request DTO containing estimates and user/project/key information.
    upstream_latency
        Time taken for the upstream provider to respond.
    gateway_overhead
        Time taken by the gateway to process the request excluding upstream latency.
    ttft
        Time to first token, if applicable.
    total_time
        Total time taken for the entire request processing.
    chat_completion
        The response object from the chat completion API, None if the request failed before receiving a response.
    status_code
        The HTTP status code of the response, defaulting to 200 for successful requests.
    failed_upstream
        Boolean indicating if the failure was due to an upstream provider issue.
    """
    usage = getattr(chat_completion, "usage", None)
    choices = getattr(chat_completion, "choices", None)

    internal_cost_final = calculate_cost(
        usage=Usage(
            input_tokens=usage.prompt_tokens if usage else 0,
            output_tokens=usage.completion_tokens if usage else 0
        ),
        model_ref=validated_request.body.model,
        provider_id=PROVIDER_ID
    ) if usage else None

    metadata = UsageLogEntry(
        key_id=validated_request.key_id,
        project_id=validated_request.project_id,
        user_id=validated_request.user_id,
        request_id=getattr(chat_completion, "id", None),
        timestamp=datetime.now(timezone.utc),
        request_type=getattr(chat_completion, "object", None),
        estimated_tokens=validated_request.estimated_tokens,
        prompt_tokens=usage.prompt_tokens if usage else None,
        completion_tokens=usage.completion_tokens if usage else None,
        total_tokens=usage.total_tokens if usage else None,
        internal_cost_estimate=validated_request.internal_cost_estimate,
        internal_cost_final=internal_cost_final,
        model=getattr(chat_completion, "model", None),
        temperature=getattr(chat_completion, "temperature", None),
        top_p=getattr(chat_completion, "top_p", None),
        top_k=getattr(chat_completion, "top_k", None),
        finish_reason=getattr(choices[0], "finish_reason", None) if choices else None,
        upstream_latency=upstream_latency,
        gateway_overhead=gateway_overhead,
        total_latency=total_time,
        ttft=ttft,
        is_streaming=getattr(chat_completion, "is_streaming", None),
        status_code=status_code
    )

    await usage_logger(metadata, failed_upstream=failed_upstream)