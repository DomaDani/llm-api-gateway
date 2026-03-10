from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from gateway.models import SQLAlchemyBase, Quota

class Limit(SQLAlchemyBase):
    __tablename__ = "limits"

    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(150), unique=True)
    description : Mapped[str] = mapped_column(String(1024))

    quotas : Mapped[list["Quota"]] = relationship("Quota", back_populates="limit")