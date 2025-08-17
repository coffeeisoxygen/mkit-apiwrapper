import app.database.session as db_session
import pytest
from sqlalchemy import inspect


async def get_table_names():
    engine = db_session.sessionmanager.engine
    if engine is None:
        raise RuntimeError("Database engine is not initialized.")
    async with engine.begin() as conn:
        return await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).get_table_names()
        )


@pytest.mark.asyncio
async def test_tables_created():
    tables = await get_table_names()
    print("Tables:", tables)
    assert "members" in tables
