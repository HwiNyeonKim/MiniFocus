from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from .base import Base
from .status import Status


class Task(Base):
    """Task model."""

    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(Status), default=Status.TODO, nullable=False)
    is_flagged = Column(Boolean, default=False, nullable=False)
    due_date = Column(DateTime, nullable=True)
    priority = Column(Integer, default=0, nullable=False)

    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)
    project = relationship("Project", back_populates="tasks")

    # Relationships
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    owner = relationship("User", back_populates="tasks")
