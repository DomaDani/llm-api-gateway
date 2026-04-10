# BASED ON: Pydantic AI Gateway's generate_api_key.js script
import base64
import os


def generate_api_key(length: int = 64) -> str:
    bytes_data = os.urandom(length)
    return base64.urlsafe_b64encode(bytes_data).rstrip(b"=").decode("utf-8")
