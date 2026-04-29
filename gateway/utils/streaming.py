import json
import time
import asyncio
from openai import AsyncStream
from openai.types.chat import ChatCompletion, ChatCompletionChunk

from gateway.logging import prepare_usage_entry
from gateway.models import ValidatedRequest
from fastapi import Request


async def stream_generator(raw_stream: AsyncStream[ChatCompletionChunk], request: Request, validated_request: ValidatedRequest):
    """
    Convert an AsyncStream of ChatCompletionChunk objects into a Server-Sent Events (SSE) stream.

    This function processes each chunk from the upstream stream, extracts relevant metadata, and yields it in a format suitable for SSE. It also handles errors gracefully by yielding an error message in the SSE format if any exceptions occur during streaming.

    Parameters
    ----------
    raw_stream : AsyncStream[ChatCompletionChunk]
        An AsyncStream of ChatCompletionChunk objects from the OpenAI package.
    request : Request
        The FastAPI request object.
    validated_request : ValidatedRequest
        The validated request DTO containing information about the request for logging and usage tracking purposes.

    Yields
    ------
    str
        A string formatted as an SSE event, containing either the chunk data or an error message.
    """
    upstream_start = time.perf_counter()
    failed_upstream = False
    ttft = None

    metadata = {}
    choices = []

    try:
        async for chunk in raw_stream:
            if ttft is None:
                ttft = time.perf_counter() - request.state.start_time
            
            chunk_metadata = chunk.model_dump(exclude={"choices"}, exclude_none=True)
            metadata.update(chunk_metadata)


            for choice in chunk.choices:
                if choice.finish_reason is not None:
                    choices.append(
                        {
                            "index": choice.index,
                            "finish_reason": choice.finish_reason,
                            "message": {"role": "assistant", "content": ""}
                        })
                    
            if chunk.usage:
                metadata["usage"] = chunk.usage.model_dump(exclude_none=True)
                break

            chunk_data = chunk.model_dump_json(exclude_unset=True)
            yield f"data: {chunk_data}\n\n"
    except Exception as e:
        failed_upstream = True
        error_data = json.dumps({"error": {"detail": str(e)}})
        yield f"data: [ERROR] {error_data}\n\n"
    finally:
        yield "data: [DONE]\n\n"

        upstream_latency = time.perf_counter() - upstream_start
        total_time = time.perf_counter() - request.state.start_time
        gateway_overhead = total_time - upstream_latency

        chat_completion = None

        if metadata:
            chat_completion_dict = {**metadata, "object": "chat.completion", "choices": choices}
            chat_completion = ChatCompletion.model_validate(chat_completion_dict)


        asyncio.create_task(prepare_usage_entry(
            request=request,
            validated_request=validated_request,
            upstream_latency=upstream_latency,
            gateway_overhead=gateway_overhead,
            ttft=ttft,
            total_time=total_time,
            chat_completion=chat_completion,
            status_code=(502 if failed_upstream else 200),
            failed_upstream=failed_upstream,
        ))
