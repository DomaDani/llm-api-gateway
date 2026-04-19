from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from .base import Base as SQLAlchemyBase
from .project_permission import ProjectPermission

class Role(SQLAlchemyBase):
    """
    ORM model representing a project membership role.

    Attributes
    ----------
    - id: The unique identifier for the role (primary key).
    - name: A unique role name.
    - description: A human-readable description of role permissions.

    Relationships
    -------------
    - permissions: The relationship to ProjectPermission rows using this role.
    """
    __tablename__ = "roles"

    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(150), unique=True)
    description : Mapped[str] = mapped_column(String(1024))

    permissions : Mapped[list["ProjectPermission"]] = relationship("ProjectPermission", back_populates="role")