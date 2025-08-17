import asyncio

import pytest
from app.database.table import create_tables
from sqlalchemy import inspect


async def get_table_names(engine):
    if engine is None:
        raise RuntimeError("Database engine is not initialized.")
    async with engine.begin() as conn:
        return await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).get_table_names()
        )


@pytest.mark.asyncio
def test_tables_created(test_sessionmanager):
    async def run():
        await create_tables(test_sessionmanager.engine)
        tables = await get_table_names(test_sessionmanager.engine)
        print("Tables:", tables)
        assert "members" in tables

    asyncio.get_event_loop().run_until_complete(run())
