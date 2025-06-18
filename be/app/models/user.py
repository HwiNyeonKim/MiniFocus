from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    """User model."""

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    # Relationships
    projects = relationship("Project", back_populates="owner")
    tasks = relationship("Task", back_populates="owner")
