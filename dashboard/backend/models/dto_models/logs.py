from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, model_validator


class UsageLogInformationRequest(BaseModel):
    project_id: int | None = None
    user_id: int | None = None
    aggregate: bool = False

    @model_validator(mode="after")
    def validate_request(self):
        if sum(x is not None for x in [self.project_id, self.user_id]) > 1:
            raise ValueError("Only one of project_id or user_id can be provided.")
        return self


class UsageLogDisplayInformation(BaseModel):
    id: int
    key_id: int
    project_id: int
    user_id: int
    request_id: str | None = None
    timestamp: datetime
    request_type: str | None = None
    estimated_tokens: int | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
    internal_cost_estimate: Decimal | None = None
    internal_cost_final: Decimal | None = None
    model: str | None = None
    temperature: float | None = None
    top_p: float | None = None
    top_k: int | None = None
    finish_reason: str | None = None
    upstream_latency: float | None = None
    gateway_overhead: float | None = None
    total_latency: float | None = None
    ttft: float | None = None
    is_streaming: bool | None = None
    status_code: int | None = None


class UsageLogAggregateDisplayInformation(BaseModel):
    time_chunk: datetime
    project_id: int
    user_id: int
    request_count: int
    total_tokens: int | None = None
    total_cost: Decimal | None = None
