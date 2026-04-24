import asyncio
import json
from types import SimpleNamespace

import pytest

from gateway.models import OpenAIMessage
import gateway.utils.price as price_mod
import gateway.utils.streaming as streaming_mod
import gateway.utils.usage as usage_mod
from tests.tools.mock_streaming import FakeAsyncStream, FakeChoice, FakeChunk, FakeUsage


def test_calculate_cost_falls_back_to_default_pricing(monkeypatch, capsys):
    """
    Tests that calculate_cost falls back to default pricing and logs a warning when calc_price raises an exception, and that it returns the default input token price multiplied by the input tokens in usage.
    Actual calculation uses the genai_prices package. As such, tests of genai_prices functionality are out of scope, but the fallback should be tested.
    """
    usage = price_mod.Usage(input_tokens=1_000_000, output_tokens=1_000_000)

    def fake_calc_price(*args, **kwargs):
        raise RuntimeError()

    monkeypatch.setattr(price_mod, "calc_price", fake_calc_price)
    monkeypatch.setattr(price_mod, "DEFAULT_INPUT_MTOKEN_PRICE", 2.5)
    monkeypatch.setattr(price_mod, "DEFAULT_OUTPUT_MTOKEN_PRICE", 9.0)

    result = price_mod.calculate_cost(usage, model_ref="model", provider_id="provider")

    assert result == 11.5
    assert "Falling back to default pricing" in capsys.readouterr().out


def test_get_token_count_joins_string_and_content_part_text(monkeypatch):
    """
    Tests that get_token_count joins plain string message content and text fields from content-part dictionaries, while ignoring non-text content parts.
    """
    captured = {}

    def fake_encode(text):
        captured["text"] = text
        return [0, 1, 2, 3, 4]

    monkeypatch.setattr(usage_mod.enc, "encode", fake_encode)

    messages = [
        OpenAIMessage(role="user", content="Vive"),
        OpenAIMessage(role="assistant", content=[
            {"type": "text", "text": " la "},
            {"type": "image_url", "image_url": {"url": "https://example.com/gecko.png"}},
        ]),
        OpenAIMessage(role="user", content="Tesherv'aals!"),
    ]

    result = usage_mod.get_token_count(messages)

    assert captured["text"] == "Vive la Tesherv'aals!"
    assert result == 5


@pytest.mark.asyncio
async def test_stream_generator_emits_chunks_and_schedules_usage(monkeypatch, validated_request):
    """
    Tests that stream_generator emits properly formatted SSE chunks from the raw stream, schedules a usage entry with the correct parameters after iteration, and handles upstream completion without marking failure.
    """
    start_time = asyncio.get_running_loop().time()
    request = SimpleNamespace(state=SimpleNamespace(start_time=start_time))
    data_chunk = FakeChunk(
        payload={"id": "chunk-1", "object": "chat.completion.chunk", "model": "test-model"},
        choices=[FakeChoice(index=0, finish_reason=None)],
    )
    terminal_chunk = FakeChunk(
        payload={"id": "chunk-1", "object": "chat.completion.chunk", "model": "test-model"},
        choices=[FakeChoice(index=0, finish_reason="stop")],
        usage=FakeUsage(prompt_tokens=2, completion_tokens=3, total_tokens=5),
    )
    raw_stream = FakeAsyncStream(chunks=[data_chunk, terminal_chunk])
    scheduled = {}

    async def fake_prepare_usage_entry(**kwargs):
        scheduled.update(kwargs)

    def fake_create_task(coro):
        scheduled["task_scheduled"] = True
        task = asyncio.get_running_loop().create_task(coro)
        scheduled["task"] = task
        return task

    monkeypatch.setattr(streaming_mod, "prepare_usage_entry", fake_prepare_usage_entry)
    monkeypatch.setattr(streaming_mod.asyncio, "create_task", fake_create_task)
    monkeypatch.setattr(streaming_mod.ChatCompletion, "model_validate", classmethod(lambda cls, data: SimpleNamespace(id=data["id"])))

    output = []
    async for item in streaming_mod.stream_generator(raw_stream, request, validated_request):
        output.append(item)

    await scheduled["task"]

    assert output == [f"data: {json.dumps(data_chunk._payload)}\n\n", "data: [DONE]\n\n"]
    assert scheduled["task_scheduled"] is True
    assert scheduled["validated_request"] is validated_request
    assert scheduled["failed_upstream"] is False
    assert scheduled["status_code"] == 200


@pytest.mark.asyncio
async def test_stream_generator_emits_error_and_marks_failure(monkeypatch, validated_request):
    """
    Tests that stream_generator emits an error chunk and a done chunk when the raw stream raises an exception on the first iteration, schedules a usage entry marked as failed with the correct parameters, and returns early without further iterations.
    """
    start_time = asyncio.get_running_loop().time()
    request = SimpleNamespace(state=SimpleNamespace(start_time=start_time))
    raw_stream = FakeAsyncStream(error=RuntimeError("upstream exploded"))
    scheduled = {}

    async def fake_prepare_usage_entry(**kwargs):
        scheduled.update(kwargs)

    def fake_create_task(coro):
        scheduled["task_scheduled"] = True
        task = asyncio.get_running_loop().create_task(coro)
        scheduled["task"] = task
        return task

    monkeypatch.setattr(streaming_mod, "prepare_usage_entry", fake_prepare_usage_entry)
    monkeypatch.setattr(streaming_mod.asyncio, "create_task", fake_create_task)
    monkeypatch.setattr(streaming_mod.ChatCompletion, "model_validate", classmethod(lambda cls, data: SimpleNamespace(id=data.get("id"))))

    output = []
    async for item in streaming_mod.stream_generator(raw_stream, request, validated_request):
        output.append(item)

    await scheduled["task"]

    assert output[0] == 'data: [ERROR] {"error": {"detail": "upstream exploded"}}\n\n'
    assert output[1] == "data: [DONE]\n\n"
    assert scheduled["task_scheduled"] is True
    assert scheduled["failed_upstream"] is True
    assert scheduled["status_code"] == 502