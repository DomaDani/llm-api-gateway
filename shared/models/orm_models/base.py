from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """
    Base declarative class for all shared SQLAlchemy ORM models.

    This class centralizes SQLAlchemy metadata registration so all ORM models
    under the shared package can be created and managed through a single base.
    """
    pass