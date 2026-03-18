from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from datetime import datetime, timezone

from .base import Base as SQLAlchemyBase
from .project_permission import ProjectPermission
from .api_key import APIKey

class User(SQLAlchemyBase):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(primary_key=True)
    email : Mapped[str] = mapped_column(String(254), unique=True)
    username : Mapped[str] = mapped_column(String(150), unique=True)
    profile_picture_url : Mapped[Optional[str]] = mapped_column(String(2048))
    password_hash : Mapped[str] = mapped_column(String(256))
    joined_date : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    last_login : Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    password_expires_at : Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    permissions : Mapped[list["ProjectPermission"]] = relationship("ProjectPermission", back_populates="user")
    api_keys : Mapped[list["APIKey"]] = relationship("APIKey", back_populates="user")

