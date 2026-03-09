from fastapi import APIRouter
from fastapi import Request, HTTPException, Depends
import time
import asyncio

from gateway.models import ValidatedRequest
from gateway.limits.quota import check_limits_costs
from gateway.logging import mock_async_logger
from gateway.clients import UpstreamClient


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
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM error: {str(e)}")
    finally:
        upstream_latency = time.perf_counter() - upstream_start
        total_time = time.perf_counter() - request.state.start_time
        gateway_overhead = total_time - upstream_latency

        usage = getattr(chat_completion, "usage", None)

        mock_metadata = {
            "place": "holder",
            "key_id": validated_request.key_id,
            "estimated_tokens": validated_request.estimated_tokens,
            "prompt_tokens": getattr(usage, "prompt_tokens", 0),
            "completion_tokens": getattr(usage, "completion_tokens", 0),
            "total_tokens": getattr(usage, "total_tokens", 0),
            "upstream_latency": round(upstream_latency, 4),
            "gateway_overhead": round(gateway_overhead, 4),
            "total_latency": round(total_time, 4)
        }

        asyncio.create_task(mock_async_logger(mock_metadata))

    return chat_completion