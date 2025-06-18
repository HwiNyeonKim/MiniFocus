"""Test configuration and fixtures."""

import asyncio
import logging
import os

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.api.dependencies import get_db
from app.main import app
from app.models import Base, Project, Task

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
TEST_DB_FILE = "./test.db"

# Create async engine for testing
engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

# Create async session factory
TestingSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()

    yield loop

    loop.close()


@pytest.fixture(scope="session")
async def test_app():
    """Create a test instance of the FastAPI application."""
    return app


@pytest.fixture(autouse=True)
async def setup_database():
    """Set up the test database before each test."""
    logger.info("Setting up test database...")

    # Ensure test.db doesn't exist before tests
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)

    # Drop all tables first
    async with engine.begin() as conn:
        logger.info("Dropping all existing tables...")
        await conn.run_sync(Base.metadata.drop_all)

        # Create all tables
        logger.info("Creating all tables...")
        # Ensure all models are imported and registered with Base.metadata
        _ = [Project, Task]  # Force model registration
        await conn.run_sync(Base.metadata.create_all)

        # Verify tables were created
        logger.info("Verifying table creation...")
        result = await conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table';")
        )
        tables = result.scalars().all()
        logger.info(f"Created tables: {tables}")

    yield

    # Cleanup after each test
    logger.info("Cleaning up test database...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    # Remove test.db file after tests
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)

    logger.info("Test database cleanup complete")


@pytest.fixture
async def test_db():
    """Create a test database session."""
    async with TestingSessionLocal() as session:
        # Start a transaction
        await session.begin()

        yield session

        # Rollback the transaction
        await session.rollback()


@pytest.fixture
async def client(test_app: FastAPI, test_db: AsyncSession):
    """Create a test client with a test database session."""

    async def override_get_db():
        yield test_db

    test_app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=test_app), base_url="http://test"
    ) as client:
        yield client

    test_app.dependency_overrides.clear()
