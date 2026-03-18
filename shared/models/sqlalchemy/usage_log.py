from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer, DateTime, Float, Boolean, Numeric
from sqlalchemy import func
from datetime import datetime
from typing import Optional

from .base import Base as SQLAlchemyBase


class UsageLog(SQLAlchemyBase):
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

    internal_cost: Mapped[Optional[float]] = mapped_column(Numeric(12, 6))

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

    is_complete : Mapped[bool] = mapped_column(Boolean)

    api_key = relationship("APIKey", lazy="select")
    project = relationship("Project", lazy="select")
    user = relationship("User", lazy="select")

