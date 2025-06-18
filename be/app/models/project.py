from sqlalchemy import Boolean, Column
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Integer, String
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

    parent_id = Column(Integer, ForeignKey("project.id"), nullable=True)
    parent = relationship(
        "Project", remote_side="Project.id", backref="children"
    )

    tasks = relationship("Task", back_populates="project")
