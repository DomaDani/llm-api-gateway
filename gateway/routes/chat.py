from fastapi import APIRouter
from fastapi import Request, HTTPException, Depends
from fastapi.responses import StreamingResponse
import time
import asyncio

from gateway.models import ValidatedRequest
from gateway.limits.quota import check_limits_costs
from gateway.logging import prepare_usage_entry
from gateway.clients import UpstreamClient
from gateway.utils import stream_generator


router  = APIRouter(prefix="/v1/chat", tags=["chat"])

def _get_upstream_client(request: Request) -> UpstreamClient:
    """
    Helper function to retrieve the upstream client from the application state.

    Parameters
    ----------
    - request: The FastAPI request object, which contains the application state.

    Returns
    -------
    - An instance of the UpstreamClient class, which is used to communicate with the upstream LLM service.
    """
    return request.app.state.upstream_client

@router.post("/completions", description="Forward a chat completion request to the upstream LLM", tags=["chat"])
async def forward_request(request: Request, validated_request: ValidatedRequest = Depends(check_limits_costs)):
    """
    Endpoint to handle chat completion requests.

    This function receives an OpenAI compatible chat completion requests, validates the key and enforces the set quotas and limits, forwards the request to the upstream LLM service, and returns the response to the client. It also handles streaming responses and logs usage data for each request.

    Parameters
    ----------
    - request: The FastAPI request object, which contains information about the incoming request and the application state.
    - validated_request: A DTO containing the validated request data, including authentication and authorization information. This is provided by the check_limits_costs dependency, which also enforces quotas and limits.

    Returns
    -------
    - If the request is not a streaming request, it returns the response from the upstream LLM service directly to the client.
    - If the request is a streaming request, it returns a StreamingResponse that streams the response from the upstream LLM service to the client as it is generated, using server-sent events (SSE).
    """
    upstream_client = _get_upstream_client(request)
    payload = validated_request.body.model_dump(exclude_unset=True)
    is_streaming = payload.get("stream", False)
    chat_completion = None

    upstream_latency = 0.0
    failed_upstream = False

    try:
        upstream_start = time.perf_counter()
        if is_streaming:
            raw_stream = await upstream_client.create_chat_completion(payload)
            status_code = 200
            return StreamingResponse(stream_generator(raw_stream=raw_stream, request=request, validated_request=validated_request), media_type="text/event-stream")
        else:
            chat_completion = await upstream_client.create_chat_completion(payload)
            status_code = 200

            upstream_latency = time.perf_counter() - upstream_start
            total_time = time.perf_counter() - request.state.start_time
            gateway_overhead = total_time - upstream_latency

            asyncio.create_task(prepare_usage_entry(
                request=request,
                validated_request=validated_request,
                upstream_latency=upstream_latency,
                gateway_overhead=gateway_overhead,
                ttft=total_time,
                total_time=total_time,
                chat_completion=chat_completion,
                status_code=status_code,
                failed_upstream=failed_upstream,
            ))
            return chat_completion
    except Exception as e:
        status_code = 502
        failed_upstream = True

        upstream_latency = time.perf_counter() - upstream_start
        total_time = time.perf_counter() - request.state.start_time
        gateway_overhead = total_time - upstream_latency

        asyncio.create_task(prepare_usage_entry(
            request=request,
            validated_request=validated_request,
            upstream_latency=upstream_latency,
            gateway_overhead=gateway_overhead,
            ttft=total_time,
            total_time=total_time,
            chat_completion=chat_completion,
            status_code=status_code,
            failed_upstream=failed_upstream,
        ))

        raise HTTPException(status_code=502, detail=f"LLM error: {str(e)}")