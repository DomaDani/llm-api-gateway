from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from gateway.models.dto_models import OpenAIRequest
from shared.models import Status

# Pydantic classes for key validation

class ValidatedRequest(BaseModel):
    key_id: int
    project_id: int
    user_id: int
    body: OpenAIRequest
    estimated_tokens: int
    internal_cost: Optional[float]