from openai import AsyncOpenAI

# Upstream client LLM Proxy.

class UpstreamClient:
    """
    A client for communicating with the upstream LLM provider. It manages the connection and provides methods to send requests to the provider's API.
    """
    def __init__(self, base_url: str, api_key: str) -> None:
        """
        Initializes the UpstreamClient with the given base URL and API key.

        Parameters
        ----------
        base_url : str
            The base URL of the upstream LLM provider's API.
        api_key : str
            The API key to authenticate with the upstream provider.
        """
        self._client = None
        self._base_url = base_url
        self._api_key = api_key

    async def startup(self) -> None:
        """
        Starts up the upstream client by initializing the AsyncOpenAI instance with the provided base URL and API key.
        This method should be called before making any requests to the upstream provider.
        """
        if self._client is None:
            self._client = AsyncOpenAI(base_url=self._base_url, api_key=self._api_key)

    async def shutdown(self) -> None:
        """
        Shuts down the upstream client by closing the AsyncOpenAI instance and setting it to None.
        This method should be called when the client is no longer needed to clean up resources.
        """
        if self._client is not None:
            await self._client.close()
            self._client = None

    async def create_chat_completion(self, payload):
        """
        Sends a request to the upstream provider to create a chat completion with the given payload.
        Handles generating the appropriate request based on whether the request is streaming or not, and includes usage information if streaming for logging.

        Parameters
        ----------
        payload : dict
            A dictionary containing the parameters for the chat completion request, such as model, messages, max_tokens, etc.
        """
        if self._client is None:
            raise RuntimeError("Upstream client not initialized.")

        return await self._client.chat.completions.create(**payload, stream_options={"include_usage": True} if payload.get("stream", False) else None)