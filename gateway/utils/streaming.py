import json
from openai import AsyncStream

async def stream_generator(raw_stream: AsyncStream):
    try:
        async for chunk in raw_stream:
            chunk_data = chunk.model_dump_json(exclude_unset=True)
            yield f"data: {chunk_data}\n\n"
    except Exception as e:
        error_data = json.dumps({"error": {"detail": str(e)}})
        yield f"data: [ERROR] {error_data}\n\n"
    finally:
        yield "data: [DONE]\n\n"