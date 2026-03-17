from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UsageLogEntry(BaseModel):
    id : int
    key_id : int
    project_id : int
    user_id : Optional[int]
    request_id : str
    timestamp : datetime

    request_type : Optional[str]

    estimated_tokens : Optional[int]

    prompt_tokens : Optional[int]
    completion_tokens : Optional[int]
    total_tokens : Optional[int]

    internal_cost : Optional[float]

    model : Optional[str]
    temperature : Optional[float]
    top_k : Optional[int]
    finish_reason : Optional[str]

    upstream_latency : Optional[float]
    gateway_overhead : Optional[float]
    total_latency : Optional[float]
    ttft : Optional[float]

    is_streaming : Optional[bool]
    status_code : Optional[int]

    is_complete : bool