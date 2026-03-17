from .openai import OpenAIRequest
from pydantic import BaseModel
from typing import Optional

# Pydantic classes for key validation

class KeyInfo(BaseModel):
    id: int
    project_id: int
    user_id: int
    limit_value: int
    spent_value: int

class ValidatedRequest(BaseModel):
    key_id: int
    project_id: int
    user_id: int

    body: OpenAIRequest
    estimated_tokens: int
    internal_cost: Optional[float]