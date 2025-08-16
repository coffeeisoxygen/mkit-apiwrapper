from contextlib import asynccontextmanager

from app.core.orchestrator import AppOrchestrator
from app.mlogg import init_logging, logger


@asynccontextmanager
async def app_lifespan(app):  # noqa: ANN001, D103
    # 1. Init logging
    init_logging()
    logger.bind(operation="app_lifespan").info("Starting application")

    # 2. Init orchestrator & services
    orchestrator = AppOrchestrator()
    await orchestrator.init_services()
    orchestrator.setup_watchers()
    await orchestrator.start_watchers()
    # 3. Simpan orchestrator di state
    app.state.orchestrator = orchestrator

    try:
        yield
    finally:
        await orchestrator.stop_watchers()
        logger.bind(operation="app_lifespan").info("Shutting down application")
