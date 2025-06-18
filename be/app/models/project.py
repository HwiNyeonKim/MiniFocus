from sqlalchemy import (
    Boolean,
    Column,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from .base import Base
from .status import Status


class Project(Base):
    """Project model."""

    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    status = Column(SQLEnum(Status), default=Status.TODO, nullable=False)
    is_flagged = Column(Boolean, default=False, nullable=False)
    is_inbox = Column(Boolean, default=False, nullable=False)

    parent_id = Column(Integer, ForeignKey("projects.id"), nullable=True)

    tasks = relationship("Task", back_populates="project")
