from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime

from .base import Base as SQLAlchemyBase

class ProjectPermission(SQLAlchemyBase):
    __tablename__ = "project_permissions"

    project_id : Mapped[int] = mapped_column(ForeignKey("projects.id"), primary_key=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    role_id : Mapped[int] = mapped_column(ForeignKey("roles.id"))
    join_date : Mapped[datetime]

    project = relationship("Project", back_populates="permissions")
    user = relationship("User", back_populates="permissions")
    role = relationship("Role", back_populates="permissions")