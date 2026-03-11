from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from datetime import datetime
from typing import Optional
from sqlalchemy import Enum as SQLAlchemyEnum

from .base import Base as SQLAlchemyBase
from .status_enum import Status

class Project(SQLAlchemyBase):
    __tablename__ = "projects"

    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(150), unique=True)
    status : Mapped[Status] = mapped_column(SQLAlchemyEnum(Status), default=Status.ACTIVE)
    created_date : Mapped[datetime]
    modified_date : Mapped[Optional[datetime]]