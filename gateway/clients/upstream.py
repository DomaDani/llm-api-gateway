from openai import AsyncOpenAI

# Upstream client LLM Proxy.

class UpstreamClient:
    def __init__(self, base_url: str, api_key: str) -> None:
        self._client = None
        self._base_url = base_url
        self._api_key = api_key

    async def startup(self) -> None:
        if self._client is None:
            self._client = AsyncOpenAI(base_url=self._base_url, api_key=self._api_key)

    async def shutdown(self) -> None:
        if self._client is not None:
            await self._client.close()
            self._client = None

    async def create_chat_completion(self, payload):
        if self._client is None:
            raise RuntimeError("Upstream client not initialized.")

        return await self._client.chat.completions.create(**payload, stream_options={"include_usage": True} if payload.get("stream", True) else None)