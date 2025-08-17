import contextlib
import uuid  # <-- add for unique IDs
from collections.abc import AsyncIterator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import get_settings
from app.custom.exc_exceptions import InternalServiceError
from app.mlogg import logger

settings = get_settings()


class DatabaseSessionManager:
    def __init__(self, host: str):
        self.engine_id = str(uuid.uuid4())  # <-- engine ID
        self.engine: AsyncEngine | None = create_async_engine(host)
        self._sessionmaker: async_sessionmaker[AsyncSession] = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )
        logger.info(f"Engine created with id={self.engine_id}")

    async def close(self):
        if self.engine is None:
            raise InternalServiceError("Engine is already disposed")
        await self.engine.dispose()
        logger.info(f"Engine disposed id={self.engine_id}")
        self.engine = None
        self._sessionmaker = None  # type: ignore

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self.engine is None:
            raise InternalServiceError("Engine not initialized")
        async with self.engine.connect() as connection:
            conn_id = str(uuid.uuid4())
            logger.info(
                f"Connection opened: engine_id={self.engine_id}, conn_id={conn_id}"
            )
            try:
                yield connection
            except SQLAlchemyError as e:
                logger.error(
                    f"Connection error: engine_id={self.engine_id}, conn_id={conn_id}, error={e}"
                )
                raise InternalServiceError from e
            finally:
                logger.info(
                    f"Connection closed: engine_id={self.engine_id}, conn_id={conn_id}"
                )

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if not self._sessionmaker:
            logger.error("Sessionmaker is not available")
            raise InternalServiceError("Sessionmaker is not available")

        session_id = str(uuid.uuid4())
        logger.info(
            f"Session opened: engine_id={self.engine_id}, session_id={session_id}"
        )
        async with self._sessionmaker() as session:
            try:
                yield session
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(
                    f"Session error: engine_id={self.engine_id}, session_id={session_id}, error={e}"
                )
                raise InternalServiceError("Could not establish session") from e
            finally:
                logger.info(
                    f"Session closed: engine_id={self.engine_id}, session_id={session_id}"
                )


sessionmanager = DatabaseSessionManager(settings.db_path)


async def get_db_session():
    """FastAPI dependency to get DB session."""
    async with sessionmanager.session() as session:
        yield session
