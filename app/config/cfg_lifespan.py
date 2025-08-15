from contextlib import asynccontextmanager

from app.core.orchestrator import AppOrchestrator
from app.mlogg import init_logging, logger


@asynccontextmanager
async def app_lifespan(app):  # noqa: ANN001, D103
    # 1. Init logging
    init_logging()
    logger.bind(operation="app_lifespan").info("Starting application")

    # 2. Init orchestrator & services
    orch = AppOrchestrator(logger)
    orch.init_services()
    orch.setup_watchers()

    # 3. Simpan orchestrator di state
    app.state.orchestrator = orch

    # 4. Start/stop orchestrator (watchers)
    await orch.start()
    try:
        yield
    finally:
        await orch.stop()
        logger.bind(operation="app_lifespan").info("Shutting down application")
