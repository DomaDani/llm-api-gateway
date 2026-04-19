from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime
from datetime import datetime, timezone

from .base import Base as SQLAlchemyBase

class ProjectPermission(SQLAlchemyBase):
    """
    ORM model representing a user's role assignment within a project.

    Attributes
    ----------
    - project_id: The foreign key to the associated project (composite primary key).
    - user_id: The foreign key to the associated user (composite primary key).
    - role_id: The foreign key to the role granted in the project.
    - join_date: The timestamp when the permission assignment was created.

    Relationships
    -------------
    - project: The relationship to the Project receiving the permission mapping.
    - user: The relationship to the User receiving the role in the project.
    - role: The relationship to the Role granted for the project membership.
    """
    __tablename__ = "project_permissions"

    project_id : Mapped[int] = mapped_column(ForeignKey("projects.id"), primary_key=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    role_id : Mapped[int] = mapped_column(ForeignKey("roles.id"))
    join_date : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    project = relationship("Project", back_populates="permissions")
    user = relationship("User", back_populates="permissions")
    role = relationship("Role", back_populates="permissions")