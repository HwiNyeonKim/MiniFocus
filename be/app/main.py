"""FastAPI application."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import items, projects
from app.config.settings import settings
from app.db.init_db import create_inbox_project, init_db
from app.db.session import AsyncSessionLocal


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler."""
    # Startup
    await init_db()
    async with AsyncSessionLocal() as session:
        await create_inbox_project(session)
    yield
    # Shutdown
    pass


def create_application() -> FastAPI:
    """Create FastAPI application."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        lifespan=lifespan,
    )

    # Set up CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_CREDENTIALS,
        allow_methods=settings.CORS_METHODS,
        allow_headers=settings.CORS_HEADERS,
    )

    # Include routers
    app.include_router(
        items.router,
        prefix=settings.API_V1_STR,
        tags=["items"],
    )
    app.include_router(
        projects.router,
        prefix=settings.API_V1_STR,
        tags=["projects"],
    )

    return app


app = create_application()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Todo API",
        "docs": "/docs",
    }
