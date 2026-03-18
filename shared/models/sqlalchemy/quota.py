from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy import Enum as SQLAlchemyEnum, DateTime
from datetime import datetime, timezone
from typing import Optional

from .base import Base as SQLAlchemyBase
from .status_enum import Status
from .period_enum import Period

class Quota(SQLAlchemyBase):
    __tablename__ = "quotas"

    id : Mapped[int] = mapped_column(primary_key=True)
    project_id : Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id"))
    user_id : Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    key_id : Mapped[Optional[int]] = mapped_column(ForeignKey("api_keys.id"))
    limit_id : Mapped[int] = mapped_column(ForeignKey("limits.id"))
    limit_value : Mapped[Optional[int]]
    period : Mapped[Period] = mapped_column(SQLAlchemyEnum(Period))
    expires_at : Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    status : Mapped[Status] = mapped_column(SQLAlchemyEnum(Status), default=Status.ACTIVE)
    allocated: Mapped[int] = mapped_column(default=0)

    project = relationship("Project", back_populates="quotas")
    api_key = relationship("APIKey", back_populates="quotas")
    user = relationship("User", back_populates="quotas")
    limit = relationship("Limit", back_populates="quotas")