import pytest
from loguru import logger


@pytest.fixture(autouse=True)
def intercept_loguru(caplog):
    handler_id = logger.add(
        sink=caplog.handler,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>",
        enqueue=False,
    )
    yield
    logger.remove(handler_id)
