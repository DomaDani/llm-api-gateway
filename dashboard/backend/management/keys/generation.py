# BASED ON: Pydantic AI Gateway's generate_api_key.js script
import base64
import os


def generate_api_key(length: int = 64) -> str:
    """
    Generate a URL-safe random API key string.
    Based on Pydantic AI Gateway's generate_api_key.js.

    Parameters
    ----------
    - length: Number of random bytes used before Base64 URL-safe encoding.

    Returns
    -------
    - A generated API key string.
    """
    bytes_data = os.urandom(length)
    return base64.urlsafe_b64encode(bytes_data).rstrip(b"=").decode("utf-8")
