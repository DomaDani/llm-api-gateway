from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from .base import Base as SQLAlchemyBase
from .quota import Quota

class Limit(SQLAlchemyBase):
    """
    ORM model representing a quota limit type's definition.

    Attributes
    ----------
    - id: The unique identifier for the limit (primary key).
    - name: A unique name for the limit type (for example 'Token Limit' or 'Request Limit').
    - description: A human-readable description of what the limit controls.

    Relationships
    -------------
    - quotas: The relationship to Quota rows that reference this limit type.
    """
    __tablename__ = "limits"

    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(150), unique=True)
    description : Mapped[str] = mapped_column(String(1024))

    quotas : Mapped[list["Quota"]] = relationship("Quota", back_populates="limit")