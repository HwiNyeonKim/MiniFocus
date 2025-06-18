from datetime import datetime

from pydantic import BaseModel

from app.models.status import Status


class TaskBase(BaseModel):
    """Base Task schema."""
    title: str
    description: str | None = None
    status: Status = Status.TODO
    is_flagged: bool = False
    due_date: datetime | None = None
    priority: int = 0  # TODO: Enum(0, 1, 2, 3)으로 관리하기


class TaskCreate(TaskBase):
    """Task creation schema."""
    pass


class TaskUpdate(BaseModel):
    """Task update schema."""
    title: str | None = None
    description: str | None = None
    status: Status | None = None
    is_flagged: bool | None = None
    due_date: datetime | None = None
    priority: int | None = None


class Task(TaskBase):
    """Task response schema."""
    id: int
    project_id: int

    class Config:
        """Pydantic config."""
        from_attributes = True
