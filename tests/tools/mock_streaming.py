import json


class FakeUsage:
    """Minimal usage payload object for streaming utility tests."""

    def __init__(self, prompt_tokens=0, completion_tokens=0, total_tokens=0):
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        self.total_tokens = total_tokens

    def model_dump(self, exclude_none=True):
        return {
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
        }


class FakeChoice:
    """Minimal choice object exposing index and finish_reason."""

    def __init__(self, index=0, finish_reason=None):
        self.index = index
        self.finish_reason = finish_reason


class FakeChunk:
    """Minimal completion chunk with dump helpers used by stream_generator."""

    def __init__(self, payload, choices, usage=None):
        self._payload = payload
        self.choices = choices
        self.usage = usage

    def model_dump(self, exclude={"choices"}, exclude_none=True):
        return dict(self._payload)

    def model_dump_json(self, exclude_unset=True):
        return json.dumps(self._payload)


class FakeAsyncStream:
    """Simple async iterator over chunks with optional first-iteration failure."""

    def __init__(self, chunks=None, error=None):
        self._chunks = list(chunks or [])
        self._error = error
        self._index = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self._error is not None and self._index == 0:
            raise self._error

        if self._index >= len(self._chunks):
            raise StopAsyncIteration

        chunk = self._chunks[self._index]
        self._index += 1
        return chunk
