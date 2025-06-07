"""Test configuration and fixtures."""
import asyncio
from typing import AsyncGenerator, Generator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.db.session import get_db
from app.main import app
from app.models.base import Base

# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Create async engine for testing
engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True,
)

# Create async session factory
TestingSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_app() -> FastAPI:
    """Create a test instance of the FastAPI application."""
    return app


@pytest.fixture(scope="session")
async def test_db() -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client(
    test_app: FastAPI, test_db: AsyncSession
) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client with a test database session."""

    async def override_get_db():
        yield test_db

    test_app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=test_app, base_url="http://test") as client:
        yield client

    test_app.dependency_overrides.clear()
