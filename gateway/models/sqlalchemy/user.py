from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from datetime import datetime

from gateway.models import SQLAlchemyBase

class User(SQLAlchemyBase):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(primary_key=True)
    email : Mapped[str] = mapped_column(String(254), unique=True)
    username : Mapped[str] = mapped_column(String(150), unique=True)
    profile_picture_url : Mapped[Optional[str]] = mapped_column(String(2048))
    password_hash : Mapped[str] = mapped_column(String(256))
    joined_date : Mapped[datetime]
    last_login : Mapped[Optional[datetime]]
    password_expires_at : Mapped[Optional[datetime]]

