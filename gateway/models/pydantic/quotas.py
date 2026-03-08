from .openai import OpenAIRequest
from pydantic import BaseModel

# Pydantic classes for key validation

class KeyInfo(BaseModel):
    id: int
    limit_value: int
    spent_value: int

class ValidatedRequest(BaseModel):
    body: OpenAIRequest
    estimated_tokens: int
    key_id: int