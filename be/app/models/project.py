from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base
from .status import Status


class Project(Base):
    """Project model."""

    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum(Status), default=Status.TODO, nullable=False)
    is_flagged = Column(Boolean, default=False, nullable=False)
    is_inbox = Column(Boolean, default=False, nullable=False)

    parent_id = Column(Integer, ForeignKey("project.id"), nullable=True)
    parent = relationship(
        "Project", remote_side="Project.id", backref="children"
    )

    tasks = relationship("Task", back_populates="project")

    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    owner = relationship("User", back_populates="projects")
