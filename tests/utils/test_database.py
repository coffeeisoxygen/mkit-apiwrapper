import app.database.session as db_session
import pytest
from app.config import get_settings
from sqlalchemy import inspect


async def get_table_names():
    async with db_session.sessionmanager.engine.begin() as conn:
        return await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).get_table_names()
        )


@pytest.mark.asyncio
async def test_database_engine_and_path():
    settings = get_settings()
    print(f"DB path for test: {settings.db_path}")
    # cek kalau test db path
    assert "test_application.db" in settings.db_path

    assert db_session.sessionmanager.engine is not None
    tables = await get_table_names()
    print(f"Tables in test DB: {tables}")
    assert isinstance(tables, list)


@pytest.mark.asyncio
async def test_members_table_exists():
    tables = await get_table_names()
    assert "members" in tables
