"""just for creating table and make it easier."""

from sqlalchemy import inspect

from app.database.session import sessionmanager
from app.models import Base
from mlogg import logger


# Create tables helper
async def create_tables():
    """Create all database tables.

    This function creates all tables defined in the SQLAlchemy models.
    """
    async with sessionmanager.engine.begin() as conn:  # type: ignore
        await conn.run_sync(
            lambda sync_conn: Base.metadata.create_all(sync_conn, checkfirst=True)
        )
        tables = await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).get_table_names()
        )
        logger.info("Tables after create_tables: %s", tables)
