"""Test project API endpoints."""
import pytest
from httpx import AsyncClient

from app.models import Project


@pytest.mark.asyncio
async def test_create_project(client: AsyncClient):
    """Test creating a new project."""
    response = await client.post(
        "/api/projects/",
        json={
            "name": "Test Project",
            "description": "This is a test project",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Project"
    assert data["description"] == "This is a test project"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_get_projects(client: AsyncClient, test_db):
    """Test getting all projects."""
    # Create test projects
    project1 = Project(name="Project 1", description="First project")
    project2 = Project(name="Project 2", description="Second project")
    test_db.add(project1)
    test_db.add(project2)
    await test_db.commit()

    response = await client.get("/api/projects/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Project 1"
    assert data[1]["name"] == "Project 2"


@pytest.mark.asyncio
async def test_get_project(client: AsyncClient, test_db):
    """Test getting a single project."""
    # Create test project
    project = Project(name="Test Project", description="Test description")
    test_db.add(project)
    await test_db.commit()

    response = await client.get(f"/api/projects/{project.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Project"
    assert data["description"] == "Test description"


@pytest.mark.asyncio
async def test_update_project(client: AsyncClient, test_db):
    """Test updating a project."""
    # Create test project
    project = Project(name="Original Name", description="Original description")
    test_db.add(project)
    await test_db.commit()

    response = await client.put(
        f"/api/projects/{project.id}",
        json={
            "name": "Updated Name",
            "description": "Updated description",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["description"] == "Updated description"


@pytest.mark.asyncio
async def test_delete_project(client: AsyncClient, test_db):
    """Test deleting a project."""
    # Create test project
    project = Project(name="Test Project", description="Test description")
    test_db.add(project)
    await test_db.commit()

    response = await client.delete(f"/api/projects/{project.id}")
    assert response.status_code == 200

    # Verify project is deleted
    response = await client.get(f"/api/projects/{project.id}")
    assert response.status_code == 404
