from pydantic import BaseModel

from app.models.status import Status


class ProjectBase(BaseModel):
    """Base Project schema."""
    name: str
    description: str | None = None
    is_inbox: bool = False
    parent_id: int | None = None
    status: Status = Status.TODO
    is_flagged: bool = False
    # TODO: priority 추가. Task와 마찬가지로 Enum(0, 1, 2, 3)으로 관리하기


class ProjectCreate(ProjectBase):
    """Project creation schema."""
    pass


class ProjectUpdate(BaseModel):
    """Project update schema."""
    name: str | None = None
    description: str | None = None
    is_inbox: bool | None = None
    status: Status | None = None
    is_flagged: bool | None = None


class Project(ProjectBase):
    """Project response schema."""
    id: int

    class Config:
        """Pydantic config."""
        from_attributes = True
