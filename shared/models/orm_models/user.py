from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from datetime import datetime, timezone

from .base import Base as SQLAlchemyBase
from .project_permission import ProjectPermission
from .api_key import APIKey
from .quota import Quota

class User(SQLAlchemyBase):
    """
    ORM model representing a platform user.

    Attributes
    ----------
    - id: The unique identifier for the user (primary key).
    - email: The unique email address used by the user.
    - username: The unique public username.
    - profile_picture_url: Optional URL to the user's profile picture.
    - password_hash: The secure hash of the user's password.
    - joined_date: The timestamp when the user account was created.
    - last_login: Optional timestamp of the user's most recent login.
    - password_expires_at: Optional timestamp for password expiration policy.

    Relationships
    -------------
    - permissions: The relationship to ProjectPermission rows for this user.
    - api_keys: The relationship to APIKey rows owned by this user.
    - quotas: The relationship to Quota rows targeting this user.
    """
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(primary_key=True)
    email : Mapped[str] = mapped_column(String(254), unique=True)
    username : Mapped[str] = mapped_column(String(150), unique=True)
    profile_picture_url : Mapped[Optional[str]] = mapped_column(String(2048))
    password_hash : Mapped[str] = mapped_column(String(256))
    joined_date : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    last_login : Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    password_expires_at : Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    permissions : Mapped[list["ProjectPermission"]] = relationship(
        "ProjectPermission",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    api_keys : Mapped[list["APIKey"]] = relationship("APIKey", back_populates="user")
    quotas : Mapped[list["Quota"]] = relationship("Quota", back_populates="user")

