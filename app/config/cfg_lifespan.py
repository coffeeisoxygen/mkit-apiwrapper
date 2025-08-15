"""settings lifespan and logging configuration."""

from contextlib import asynccontextmanager

from app.mlogg import init_logging, logger


@asynccontextmanager
async def app_lifespan(app):  # noqa: ANN001, ARG001, D103, RUF029
    init_logging()
    logger.bind(operation="app_lifespan").info("Starting application")
    yield
    logger.bind(operation="app_lifespan").info("Shutting down application...")
