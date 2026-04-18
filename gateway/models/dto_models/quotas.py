from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from gateway.models.dto_models import OpenAIRequest
from shared.models import Status

# Pydantic classes for key validation

class ValidatedRequest(BaseModel):
    """
    A class representing a request made to the gateway that has been validated for authentication and authorization.
    """
    key_id: int
    project_id: int
    user_id: int
    body: OpenAIRequest
    estimated_tokens: int
    internal_cost_estimate: Optional[float]