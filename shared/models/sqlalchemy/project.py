from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Enum as SQLAlchemyEnum, DateTime

from .base import Base as SQLAlchemyBase
from .status_enum import Status
from .project_permission import ProjectPermission
from .api_key import APIKey
from .quota import Quota

class Project(SQLAlchemyBase):
    __tablename__ = "projects"

    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(150), unique=True)
    status : Mapped[Status] = mapped_column(SQLAlchemyEnum(Status), default=Status.ACTIVE)
    created_date : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    modified_date : Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=datetime.now(timezone.utc))

    permissions : Mapped[list["ProjectPermission"]] = relationship("ProjectPermission", back_populates="project")
    api_keys : Mapped[list["APIKey"]] = relationship("APIKey", back_populates="project")
    quotas : Mapped[list["Quota"]] = relationship("Quota", back_populates="project")