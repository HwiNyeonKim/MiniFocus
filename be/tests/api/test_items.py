import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Project, Status, Task


@pytest.mark.asyncio
@pytest.mark.parametrize("description", ["test description", None])
async def test_create_task(
    client: AsyncClient,
    test_db: AsyncSession,
    description,
):
    project = Project(
        name="Test Project",
        description="Test Description",
        is_inbox=False,
    )
    test_db.add(project)
    await test_db.commit()

    response = await client.post(
        url=f"/api/v1/projects/{project.id}/tasks/",
        json={
            "title": "Test Item",
            "description": description,
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Test Item"
    assert data["description"] == description
    assert data["due_date"] is None
    assert data["status"] == Status.TODO
    assert data["is_flagged"] is False
    assert data["priority"] == 0
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_get_tasks(client: AsyncClient, test_db: AsyncSession):
    project = Project(
        name="Test Project",
        description="Test Description",
        is_inbox=False,
    )
    test_db.add(project)
    await test_db.commit()
    await test_db.refresh(project)

    task1 = Task(
        title="Test Item",
        description="Test Description",
        project_id=project.id,
    )
    test_db.add(task1)
    await test_db.commit()
    await test_db.refresh(task1)

    task2 = Task(
        title="Test Item 2",
        description="Test Description 2",
        project_id=project.id,
    )
    test_db.add(task2)
    await test_db.commit()
    await test_db.refresh(task2)

    response = await client.get(
        url=f"/api/v1/projects/{project.id}/tasks/",
    )
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2

    assert data[0]["title"] == "Test Item"
    assert data[0]["description"] == "Test Description"
    assert data[0]["status"] == Status.TODO
    assert data[0]["is_flagged"] is False
    assert data[0]["priority"] == 0
    assert "id" in data[0]
    assert "created_at" in data[0]
    assert "updated_at" in data[0]

    assert data[1]["title"] == "Test Item 2"
    assert data[1]["description"] == "Test Description 2"
    assert data[1]["status"] == Status.TODO
    assert data[1]["is_flagged"] is False
    assert data[1]["priority"] == 0
    assert "id" in data[1]
    assert "created_at" in data[1]
    assert "updated_at" in data[1]


@pytest.mark.asyncio
async def test_update_task(client: AsyncClient, test_db: AsyncSession):
    project = Project(
        name="Test Project",
        description="Test Description",
        is_inbox=False,
    )
    test_db.add(project)
    await test_db.commit()
    await test_db.refresh(project)

    task = Task(
        title="Test Item",
        description="Test Description",
        project_id=project.id,
    )
    test_db.add(task)
    await test_db.commit()
    await test_db.refresh(task)

    response = await client.put(
        url=f"/api/v1/projects/{project.id}/tasks/{task.id}",
        json={
            "title": "Updated Item",
            "description": "Updated Description",
            "status": Status.DONE,
        },
    )
    assert response.status_code == 200
    data = response.json()

    assert data["title"] == "Updated Item"
    assert data["description"] == "Updated Description"
    assert data["status"] == Status.DONE
    assert data["priority"] == 0
    assert data["project_id"] == project.id
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_delete_task(client: AsyncClient, test_db: AsyncSession):
    project = Project(
        name="Test Project",
        description="Test Description",
        is_inbox=False,
    )
    test_db.add(project)
    await test_db.commit()
    await test_db.refresh(project)

    task = Task(
        title="Test Item",
        description="Test Description",
        project_id=project.id,
    )
    test_db.add(task)
    await test_db.commit()
    await test_db.refresh(task)

    response = await client.delete(
        url=f"/api/v1/projects/{project.id}/tasks/{task.id}",
    )
    assert response.status_code == 200
    data = response.json()

    assert data["message"] == "Task deleted successfully"

    # Verify the task is deleted
    response = await client.get(
        url=f"/api/v1/projects/{project.id}/tasks/{task.id}",
    )
    assert response.status_code == 404
