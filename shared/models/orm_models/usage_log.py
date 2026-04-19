from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer, DateTime, Float, Boolean, Numeric
from sqlalchemy import func
from datetime import datetime
from typing import Optional

from .base import Base as SQLAlchemyBase


class UsageLog(SQLAlchemyBase):
    """
    ORM model representing a single gateway usage record.

    Attributes
    ----------
    - id: The unique identifier for the usage log entry (primary key).
    - key_id: The foreign key to the API key used for the request.
    - project_id: The foreign key to the project billed for the request.
    - user_id: The foreign key to the user associated with the request.
    - request_id: Optional unique upstream or gateway request identifier.
    - timestamp: The timestamp when the request was recorded.
    - request_type: Optional request category.
    - estimated_tokens: Optional token estimate captured before completion.
    - prompt_tokens: Optional prompt token count.
    - completion_tokens: Optional completion token count.
    - total_tokens: Optional total and finalised token count.
    - internal_cost_estimate: Optional pre-finalized internal cost estimate.
    - internal_cost_final: Optional finalised internal cost.
    - model: Optional model name used for the request.
    - temperature: Optional sampling temperature parameter.
    - top_p: Optional nucleus sampling parameter.
    - top_k: Optional top-k sampling parameter.
    - finish_reason: Optional completion stop reason.
    - upstream_latency: Optional measured upstream service latency.
    - gateway_overhead: Optional measured gateway processing overhead.
    - total_latency: Optional total end-to-end request latency.
    - ttft: Optional time-to-first-token for streaming responses.
    - is_streaming: Optional flag indicating if response was streamed.
    - status_code: Optional resulting HTTP status code.

    Relationships
    -------------
    - api_key: The relationship to the APIKey associated with this request.
    - project: The relationship to the Project associated with this request.
    - user: The relationship to the User associated with this request.
    """
    __tablename__ = "usage_logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    key_id: Mapped[int] = mapped_column(ForeignKey("api_keys.id"))
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    request_id: Mapped[Optional[str]] = mapped_column(String(255), unique=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    request_type: Mapped[Optional[str]] = mapped_column(String(50))

    estimated_tokens : Mapped[Optional[int]] = mapped_column(Integer)

    prompt_tokens: Mapped[Optional[int]] = mapped_column(Integer)
    completion_tokens: Mapped[Optional[int]] = mapped_column(Integer)
    total_tokens: Mapped[Optional[int]] = mapped_column(Integer)

    internal_cost_estimate: Mapped[Optional[float]] = mapped_column(Numeric(12, 6))
    internal_cost_final: Mapped[Optional[float]] = mapped_column(Numeric(12, 6))

    model: Mapped[Optional[str]] = mapped_column(String(255))
    temperature: Mapped[Optional[float]] = mapped_column(Float)
    top_p: Mapped[Optional[float]] = mapped_column(Float)
    top_k: Mapped[Optional[int]] = mapped_column(Integer)
    finish_reason: Mapped[Optional[str]] = mapped_column(String(64))

    upstream_latency: Mapped[Optional[float]] = mapped_column(Float)
    gateway_overhead: Mapped[Optional[float]] = mapped_column(Float)
    total_latency: Mapped[Optional[float]] = mapped_column(Float)
    ttft: Mapped[Optional[float]] = mapped_column(Float)

    is_streaming: Mapped[Optional[bool]] = mapped_column(Boolean)
    status_code: Mapped[Optional[int]] = mapped_column(Integer)

    api_key = relationship("APIKey", lazy="select")
    project = relationship("Project", lazy="select")
    user = relationship("User", lazy="select")

