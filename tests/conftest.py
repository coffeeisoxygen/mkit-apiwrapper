import pytest
from dotenv import load_dotenv
import app.database.session as db_session
from app.database.table import create_tables
from app.models import Base
from loguru import logger
from app.config import get_settings
from pathlib import Path

PATHTOTESTENV = Path(__file__).parent.parent / ".env.test"


# --- SessionManager Fixture ---
@pytest.fixture(scope="session")
def test_sessionmanager():
    from app.database.session import sessionmanager

    return sessionmanager


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
    db_session.sessionmanager = db_session.DatabaseSessionManager(settings.db_path)
    logger.info(f"Engine id after re-init: {id(db_session.sessionmanager.engine)}")
    import asyncio

    asyncio.get_event_loop().run_until_complete(
        create_tables(db_session.sessionmanager.engine)
    )


# --- Logging ---
from .fixtures.logging import intercept_loguru


# --- Database tables ---
@pytest.fixture(scope="session", autouse=True)
async def setup_test_db():
    yield
    if db_session.sessionmanager.engine is not None:
        async with db_session.sessionmanager.engine.begin() as conn:
            await conn.run_sync(lambda sync_conn: Base.metadata.drop_all(sync_conn))


# --- Fixtures data ---
from tests.fixtures.data import test_file_path, valid_members_data, valid_cities_data
