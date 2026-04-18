import tiktoken
from gateway.models import OpenAIMessage
from typing import List

# Utilities for calculating usage metrics.

enc = tiktoken.get_encoding("o200k_base")

def get_token_count(messages: List[OpenAIMessage]) -> int:
    """
    Calculate the total number of tokens in a list of OpenAIMessage objects.

    This function uses the tiktoken library to encode the content of the messages and counts the total number of tokens.

    Parameters
    ----------
    - messages: A list of OpenAIMessage DTOs, where each message contains a 'content' field that can be a string.

    Returns
    -------
    - An integer representing the total number of tokens in the messages.
    """
    text = "".join([m.content for m in messages if isinstance(m.content, str)])
    
    return len(enc.encode(text))