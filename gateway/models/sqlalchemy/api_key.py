from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from datetime import datetime
from sqlalchemy import Enum as SQLAlchemyEnum

from gateway.models import SQLAlchemyBase, Status

class APIKey(SQLAlchemyBase):
    __tablename__ = "api_keys"

    id : Mapped[int] = mapped_column(primary_key=True)
    project_id : Mapped[int] = mapped_column(ForeignKey("projects.id"))
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    name : Mapped[str] = mapped_column(String(150))
    fingerprint : Mapped[str] = mapped_column(String(16), unique=True)
    key_hash : Mapped[str] = mapped_column(String(256))
    create_date : Mapped[datetime]
    status : Mapped[Status] = mapped_column(SQLAlchemyEnum(Status), default=Status.ACTIVE)

    project = relationship("Project", back_populates="api_keys")
    user = relationship("User", back_populates="api_keys")