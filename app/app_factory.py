from fastapi import FastAPI

from app.api.routes.tasks import router as tasks_router
from app.api.routes.health import router as health_router
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        version="1.1.0",
    )

    app.include_router(tasks_router)
    app.include_router(health_router)

    return app