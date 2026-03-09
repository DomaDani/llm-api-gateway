from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from datetime import datetime
from typing import Optional
from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum

from gateway.models import SQLAlchemyBase

class ProjectStatus(Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"

class Project(SQLAlchemyBase):
    __tablename__ = "projects"

    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(150), unique=True)
    status : Mapped[ProjectStatus] = mapped_column(SQLAlchemyEnum(ProjectStatus))
    created_date : Mapped[datetime]
    modified_date : Mapped[Optional[datetime]]