from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from gateway.models import SQLAlchemyBase, ProjectPermission

class Role(SQLAlchemyBase):
    __tablename__ = "roles"

    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(150), unique=True)
    description : Mapped[str] = mapped_column(String(1024))

    permissions : Mapped[list["ProjectPermission"]] = relationship("ProjectPermission", back_populates="role")