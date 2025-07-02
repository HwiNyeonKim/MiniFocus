from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Project as ProjectModel
from app.models import Task as TaskModel
from app.schemas import Task, TaskCreate, TaskUpdate, User

from ..dependencies import get_db, get_current_user

router = APIRouter()


@router.get("/projects/{project_id}/tasks/", response_model=List[Task])
async def get_tasks(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all tasks for a project."""
    project = await db.get(ProjectModel, project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    # Query tasks directly instead of accessing through relationship
    tasks = await db.execute(
        select(TaskModel).where(TaskModel.project_id == project_id)
    )
    tasks = tasks.scalars().all()

    return [Task.model_validate(task) for task in tasks]


@router.post("/projects/{project_id}/tasks/", response_model=Task)
async def create_task(
    project_id: int,
    task: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new task for a project."""
    project = await db.get(ProjectModel, project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    db_task = TaskModel(**task.model_dump())
    db_task.project_id = project_id
    db_task.owner_id = current_user.id
    db.add(db_task)

    await db.commit()
    await db.refresh(db_task)

    return Task.model_validate(db_task)


@router.get("/projects/{project_id}/tasks/{task_id}", response_model=Task)
async def get_task(
    project_id: int,
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific task for a project."""
    project = await db.get(ProjectModel, project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    task = await db.get(TaskModel, task_id)

    if not task or task.project_id != project_id:
        raise HTTPException(status_code=404, detail="Task not found")

    return Task.model_validate(task)


@router.put("/projects/{project_id}/tasks/{task_id}", response_model=Task)
async def update_task(
    project_id: int,
    task_id: int,
    task: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a specific task for a project."""
    project = await db.get(ProjectModel, project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    db_task = await db.get(TaskModel, task_id)

    if not db_task or db_task.project_id != project_id:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)

    await db.commit()
    await db.refresh(db_task)

    return Task.model_validate(db_task)


@router.delete(
    "/projects/{project_id}/tasks/{task_id}", response_model=dict[str, str]
)
async def delete_task(
    project_id: int,
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a task."""
    project = await db.get(ProjectModel, project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    db_task = await db.get(TaskModel, task_id)

    if not db_task or db_task.project_id != project_id:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.delete(db_task)
    await db.commit()

    return {"message": "Task deleted successfully"}
