from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1 import bob, checkpoints, projects, workflows
from .config import settings


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, version=settings.app_version)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(projects.router, prefix="/api/v1")
    app.include_router(checkpoints.router, prefix="/api/v1")
    app.include_router(workflows.router, prefix="/api/v1")
    app.include_router(bob.router, prefix="/api/v1")

    @app.get("/health", tags=["system"])
    def health():
        return {
            "status": "ok",
            "app": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment,
        }

    return app


app = create_app()
