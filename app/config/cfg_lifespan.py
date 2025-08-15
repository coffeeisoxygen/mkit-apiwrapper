from contextlib import asynccontextmanager
from pathlib import Path

from app.core.async_watcher import AsyncFileWatcher
from app.core.orchestrator import AppOrchestrator
from app.mlogg import init_logging, logger


@asynccontextmanager
async def app_lifespan(app):
    # 1. Init logging
    init_logging()
    logger.bind(operation="app_lifespan").info("Starting application")

    # 2. Init orchestrator & services
    orch = AppOrchestrator(logger)
    orch.init_services()

    # 3. Setup watcher async
    watcher = AsyncFileWatcher()
    watcher.add_watch(Path("data/members.yaml"), orch.get_member_service().load_members)

    # nanti bisa tambah product/module watcher
    # watcher.add_watch(Path("data/products.yaml"), orch.get_product_service().load_products)

    # 4. Start watcher async via orchestrator
    await orch.start(watcher)

    # simpan state supaya route bisa akses service/watcher
    app.state.orchestrator = orch
    app.state.watcher = watcher

    try:
        yield
    finally:
        await watcher.stop()
        logger.bind(operation="app_lifespan").info("Shutting down application")
