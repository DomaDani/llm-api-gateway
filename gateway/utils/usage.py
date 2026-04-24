import tiktoken
from gateway.models import OpenAIMessage
from typing import List

# Utilities for calculating usage metrics.

enc = tiktoken.get_encoding("o200k_base")


def _extract_message_text(content) -> str:
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str):
                    parts.append(text)
        return "".join(parts)

    return ""


def get_token_count(messages: List[OpenAIMessage]) -> int:
    """
    Calculate the total number of tokens in a list of OpenAIMessage objects.

    This function uses the tiktoken library to encode the content of the messages and counts the total number of tokens.

    Parameters
    ----------
    - messages: A list of OpenAIMessage DTOs, where each message contains a 'content' field that can be a string or an array of content-part dictionaries.

    Returns
    -------
    - An integer representing the total number of tokens in the messages.
    """
    text = "".join(_extract_message_text(m.content) for m in messages)
    
    return len(enc.encode(text))