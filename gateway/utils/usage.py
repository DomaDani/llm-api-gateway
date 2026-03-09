import tiktoken
from gateway.models import OpenAIMessage
from typing import List

# Utilities for calculating usage metrics.

enc = tiktoken.get_encoding("o200k_base")

def get_token_count(messages: List[OpenAIMessage]) -> int:
    text = "".join([m.content for m in messages if isinstance(m.content, str)])
    
    return len(enc.encode(text))