import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Project


@pytest.mark.asyncio
@pytest.mark.parametrize("description", ["test description", None])
async def test_create_project(
    client: AsyncClient, test_db: AsyncSession, description
):
    response = await client.post(
        "/api/v1/projects/",
        json={
            "name": "Create Test Project",
            "description": description,
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Create Test Project"
    assert data["description"] == description
    assert data["is_inbox"] is False
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_get_projects(client: AsyncClient, test_db: AsyncSession):
    projects = [
        Project(
            name=f"List Test Project {i}",
            description=f"Test Description {i}",
            is_inbox=False,
        )
        for i in range(3)
    ]
    for project in projects:
        test_db.add(project)

    await test_db.commit()

    response = await client.get("/api/v1/projects/")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 3
    for i, project in enumerate(data):
        assert project["name"] == f"List Test Project {i}"
        assert project["description"] == f"Test Description {i}"
        assert project["is_inbox"] is False
        assert "id" in project
        assert "created_at" in project
        assert "updated_at" in project


@pytest.mark.asyncio
async def test_get_project(client: AsyncClient, test_db: AsyncSession):
    project = Project(
        name="Get Test Project",
        description="Test Description",
        is_inbox=False,
    )
    test_db.add(project)
    await test_db.commit()
    await test_db.refresh(project)

    response = await client.get(f"/api/v1/projects/{project.id}")
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Get Test Project"
    assert data["description"] == "Test Description"
    assert data["is_inbox"] is False
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_update_project(client: AsyncClient, test_db: AsyncSession):
    project = Project(
        name="Update Test Project",
        description="Test Description",
        is_inbox=False,
    )
    test_db.add(project)
    await test_db.commit()
    await test_db.refresh(project)

    response = await client.put(
        f"/api/v1/projects/{project.id}",
        json={
            "name": "Updated Project",
            "description": "Updated Description",
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Updated Project"
    assert data["description"] == "Updated Description"
    assert data["is_inbox"] is False
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_delete_project(client: AsyncClient, test_db: AsyncSession):
    project = Project(
        name="Delete Test Project",
        description="Test Description",
        is_inbox=False,
    )
    test_db.add(project)
    await test_db.commit()
    await test_db.refresh(project)

    response = await client.delete(f"/api/v1/projects/{project.id}")
    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "Project deleted successfully"

    # Verify the project is deleted
    response = await client.get(f"/api/v1/projects/{project.id}")
    assert response.status_code == 404
