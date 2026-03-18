from pydantic import BaseModel
from typing import Optional

from gateway.models import OpenAIRequest
from shared.models.sqlalchemy import APIKey

# Pydantic classes for key validation

class KeyInfo(BaseModel):
    id: int
    project_id: int
    user_id: int
    limit_value: int
    spent_value: int

class ValidatedRequest(BaseModel):
    api_key: APIKey
    body: OpenAIRequest
    estimated_tokens: int
    internal_cost: Optional[float]