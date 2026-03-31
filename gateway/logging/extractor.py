from datetime import datetime, timezone
import time
from fastapi import Request

from gateway.models import ValidatedRequest, UsageLogEntry
from gateway.logging import usage_logger

async def prepare_usage_entry(request: Request, validated_request: ValidatedRequest, upstream_latency, gateway_overhead, total_time, chat_completion=None, status_code=200, failed_upstream=False):
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
        status_code=status_code
    )

    await usage_logger(metadata, failed_upstream=failed_upstream)