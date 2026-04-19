from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from datetime import datetime, timezone
from sqlalchemy import Enum as SQLAlchemyEnum, DateTime

from .base import Base as SQLAlchemyBase
from .status_enum import Status
from .quota import Quota

class APIKey(SQLAlchemyBase):
    """
    ORM model representing an API key in the database.

    Attributes
    ----------
    - id: The unique identifier for the API key (primary key).
    - project_id: The foreign key linking to the associated project.
    - user_id: The foreign key linking to the associated user, nullable for keys not tied to a specific user.
    - name: A human-readable name for the API key.
    - fingerprint: A unique fingerprint derived from the API key for quick lookup.
    - key_hash: A secure hash of the API key for verification purposes.
    - create_date: The timestamp when the API key was created.
    - status: The current status of the API key (e.g., active, inactive).

    Relationships
    -------------
    - project: The relationship to the Project model, indicating which project this API key belongs to.
    - user: The relationship to the User model, indicating which user this API key belongs to (if applicable).
    - quotas: The relationship to the Quota model, representing the quotas directly targeting the API key.
    """
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