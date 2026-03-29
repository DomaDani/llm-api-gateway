from fastapi import APIRouter
from fastapi import Request, HTTPException, Depends
import time
import asyncio
from datetime import datetime, timezone

from gateway.models import ValidatedRequest
from gateway.limits.quota import check_limits_costs
from gateway.logging import usage_logger
from gateway.clients import UpstreamClient
from gateway.models.dto_models.usage import UsageLogEntry


router  = APIRouter(prefix="/v1/chat", tags=["chat"])

def get_upstream_client(request: Request) -> UpstreamClient:
    return request.app.state.upstream_client

@router.post("/completions", description="Forward a chat completion request to the upstream LLM", tags=["chat"])
async def forward_request(request: Request, validated_request: ValidatedRequest = Depends(check_limits_costs)):
    upstream_client = get_upstream_client(request)
    payload = validated_request.body.model_dump(exclude_unset=True)
    chat_completion = None

    upstream_latency = 0.0

    try:
        upstream_start = time.perf_counter()
        chat_completion = await upstream_client.create_chat_completion(payload)
        status_code = 200
    except Exception as e:
        status_code = 502
        raise HTTPException(status_code=502, detail=f"LLM error: {str(e)}")
    finally:
        upstream_latency = time.perf_counter() - upstream_start
        total_time = time.perf_counter() - request.state.start_time
        gateway_overhead = total_time - upstream_latency

        usage = getattr(chat_completion, "usage", None)
        choices = getattr(chat_completion, "choices", None)

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
            internal_cost=validated_request.internal_cost,
            model=getattr(chat_completion, "model", None),
            temperature=getattr(chat_completion, "temperature", None),
            top_p=getattr(chat_completion, "top_p", None),
            top_k=getattr(chat_completion, "top_k", None),
            finish_reason=getattr(choices[0], "finish_reason", None) if choices else None,
            upstream_latency=upstream_latency,
            gateway_overhead=gateway_overhead,
            total_latency=total_time,
            ttft=time.perf_counter() - request.state.start_time,
            is_streaming=getattr(chat_completion, "is_streaming", None),
            status_code=status_code,
            is_complete=True,
        )


        asyncio.create_task(usage_logger(metadata))

    return chat_completion