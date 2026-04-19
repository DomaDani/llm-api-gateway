from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy import Enum as SQLAlchemyEnum, DateTime
from datetime import datetime, timezone
from typing import Optional

from .base import Base as SQLAlchemyBase
from .status_enum import Status
from .period_enum import Period

class Quota(SQLAlchemyBase):
    """
    ORM model representing quota allocation and reset state.

    Attributes
    ----------
    - id: The unique identifier for the quota entry (primary key).
    - project_id: Optional foreign key to the project targeted by this quota.
    - user_id: Optional foreign key to the user targeted by this quota.
    - key_id: Optional foreign key to the API key targeted by this quota.
    - limit_id: The foreign key to the limit type being constrained.
    - limit_value: The allocated maximum value for the configured limit and period.
    - period: The reset period for the quota.
    - expires_at: Optional timestamp when this quota definition expires.
    - status: The current lifecycle state of the quota.
    - allocated: The currently consumed amount within the active period.
    - next_reset: The timestamp when allocated usage resets.

    Relationships
    -------------
    - project: The relationship to the Project this quota directly applies to.
    - api_key: The relationship to the APIKey this quota directly applies to.
    - user: The relationship to the User this quota directly applies to.
    - limit: The relationship to the Limit definition for this quota.
    """
    __tablename__ = "quotas"

    id : Mapped[int] = mapped_column(primary_key=True)
    project_id : Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id"))
    user_id : Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    key_id : Mapped[Optional[int]] = mapped_column(ForeignKey("api_keys.id"))
    limit_id : Mapped[int] = mapped_column(ForeignKey("limits.id"))
    limit_value : Mapped[Optional[float]]
    period : Mapped[Period] = mapped_column(SQLAlchemyEnum(Period))
    expires_at : Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    status : Mapped[Status] = mapped_column(SQLAlchemyEnum(Status), default=Status.ACTIVE)
    allocated: Mapped[float] = mapped_column(default=0)
    next_reset: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)

    project = relationship("Project", back_populates="quotas")
    api_key = relationship("APIKey", back_populates="quotas")
    user = relationship("User", back_populates="quotas")
    limit = relationship("Limit", back_populates="quotas")