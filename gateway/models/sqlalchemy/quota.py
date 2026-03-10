from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy import Enum as SQLAlchemyEnum
from datetime import datetime
from typing import Optional

from gateway.models import SQLAlchemyBase, Status, Period

class Quota(SQLAlchemyBase):
    __tablename__ = "quotas"

    id : Mapped[int] = mapped_column(primary_key=True)
    project_id : Mapped[int] = mapped_column(ForeignKey("projects.id"))
    key_id : Mapped[int] = mapped_column(ForeignKey("api_keys.id"))
    limit_id : Mapped[int] = mapped_column(ForeignKey("limits.id"))
    limit_value : Mapped[int]
    period : Mapped[Period] = mapped_column(SQLAlchemyEnum(Period))
    expires_at : Mapped[Optional[datetime]]
    status : Mapped[Status] = mapped_column(SQLAlchemyEnum(Status), default=Status.ACTIVE)

    project = relationship("Project", back_populates="quotas")
    api_key = relationship("APIKey", back_populates="quotas")
    limit = relationship("Limit", back_populates="quotas")