from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from datetime import datetime, timezone
from sqlalchemy import Enum as SQLAlchemyEnum, DateTime

from .base import Base as SQLAlchemyBase
from .status_enum import Status
from .quota import Quota

class APIKey(SQLAlchemyBase):
    __tablename__ = "api_keys"

    id : Mapped[int] = mapped_column(primary_key=True)
    project_id : Mapped[int] = mapped_column(ForeignKey("projects.id"))
    user_id : Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    name : Mapped[str] = mapped_column(String(150))
    fingerprint : Mapped[str] = mapped_column(String(16), unique=True)
    key_hash : Mapped[str] = mapped_column(String(256))
    create_date : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    status : Mapped[Status] = mapped_column(SQLAlchemyEnum(Status), default=Status.ACTIVE)

    project = relationship("Project", back_populates="api_keys")
    user = relationship("User", back_populates="api_keys")
    quotas : Mapped[list["Quota"]] = relationship("Quota", back_populates="api_key")