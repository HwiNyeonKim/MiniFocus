from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.endpoints import auth, projects, tasks
from .config.settings import settings
from .db import AsyncSessionLocal, create_inbox_project, init_db


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
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(
        tasks.router,
        prefix=settings.API_V1_STR,
        tags=["tasks"],
    )
    app.include_router(
        projects.router,
        prefix=settings.API_V1_STR,
        tags=["projects"],
    )

    app.include_router(
        auth.router,
        prefix=settings.API_V1_STR,
        tags=["auth"],
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
