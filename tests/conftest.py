import pytest


# --- SessionManager Fixture ---
@pytest.fixture(scope="session")
def test_sessionmanager():
    from app.database.session import sessionmanager

    return sessionmanager


from pathlib import Path
import pytest
import yaml
from dotenv import load_dotenv
from sqlalchemy import inspect

import app.database.session as db_session
from app.database.table import create_tables
from app.models import Base
from app.models.member import Member

from loguru import logger
from app.config import get_settings

PATHTOTESTENV = Path(__file__).parent.parent / ".env.test"


# --- Environment ---
@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    load_dotenv(dotenv_path=PATHTOTESTENV, override=True)
    get_settings.cache_clear()
    settings = get_settings()
    import os

    logger.info(f"[conftest] DB path: {settings.db_path}")
    logger.info(f"[conftest] CWD: {os.getcwd()}")
    assert settings.app_env == "TESTING"
    # re-init DB engine pakai test DB
    db_session.sessionmanager = db_session.DatabaseSessionManager(settings.db_path)
    logger.info(f"Engine id after re-init: {id(db_session.sessionmanager.engine)}")
    # Panggil create_tables setelah engine di-reinit
    import asyncio

    asyncio.get_event_loop().run_until_complete(
        create_tables(db_session.sessionmanager.engine)
    )


# --- Logging ---
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


# --- Database tables ---
@pytest.fixture(scope="session", autouse=True)
async def setup_test_db():
    yield
    if db_session.sessionmanager.engine is not None:
        async with db_session.sessionmanager.engine.begin() as conn:
            await conn.run_sync(lambda sync_conn: Base.metadata.drop_all(sync_conn))


# --- Fixtures data ---
@pytest.fixture(scope="session")
def test_file_path():
    return Path(__file__).parent / "data"


@pytest.fixture(scope="session")
def valid_members_data(test_file_path):
    yaml_path = test_file_path / "members_valid.yaml"
    with open(yaml_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["members"]


@pytest.fixture(scope="session")
def valid_cities_data(test_file_path):
    yaml_path = test_file_path / "cities_valid.yaml"
    with open(yaml_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["cities"]
