from typing import Any, TypeVar

from app.custom.exc_exceptions import RepositoryExcpError
from app.mlogg import logger

T = TypeVar("T")  # entity type


class BaseRepository[T]:
    """Base repository dengan fail-fast, contextual logging, dan RepositoryExcpError."""

    repo_name: str = "BaseRepository"

    def __init__(self, datamanager: Any):
        self._datamanager = datamanager
        self._log = logger.bind(repo=self.repo_name)

    def add(self, key: str, entity: T):
        log = self._log.bind(operation="add", key=key)
        try:
            self._datamanager.add_item(key, entity)
            log.info("Entity ditambahkan")
        except Exception as e:
            log.exception("Gagal add entity")
            raise RepositoryExcpError(f"{self.repo_name} gagal add") from e

    def add_bulk(self, items: dict[str, T]):
        log = self._log.bind(operation="add_bulk", count=len(items))
        try:
            for key, entity in items.items():
                self.add(key, entity)  # fail-fast per item
            log.info("Bulk entities ditambahkan")
        except Exception as e:
            log.exception("Gagal add bulk")
            raise RepositoryExcpError(f"{self.repo_name} gagal add_bulk") from e

    def get(self, key: str) -> T | None:
        log = self._log.bind(operation="get", key=key)
        try:
            entity = self._datamanager.get_item(key)
            if entity is None:
                log.warning("Entity tidak ditemukan")
            else:
                log.info("Entity ditemukan")
        except Exception as e:
            log.exception("Gagal get entity")
            raise RepositoryExcpError(f"{self.repo_name} gagal get") from e
        else:
            return entity

    def get_all(self) -> list[T]:
        log = self._log.bind(operation="get_all")
        try:
            entities = list(self._datamanager.get_data().values())
            log.info(f"Total entities: {len(entities)}")
        except Exception as e:
            log.exception("Gagal get_all")
            raise RepositoryExcpError(f"{self.repo_name} gagal get_all") from e
        else:
            return entities

    def delete(self, key: str):
        log = self._log.bind(operation="delete", key=key)
        try:
            self._datamanager.remove_item(key)
            log.info("Entity dihapus")
        except Exception as e:
            log.exception("Gagal delete")
            raise RepositoryExcpError(f"{self.repo_name} gagal delete") from e

    def exists(self, key: str) -> bool:
        log = self._log.bind(operation="exists", key=key)
        try:
            exists = key in self._datamanager.get_data()
            log.info(f"Exists: {exists}")
        except Exception as e:
            log.exception("Gagal cek exists")
            raise RepositoryExcpError(f"{self.repo_name} gagal exists") from e
        else:
            return exists

    def count(self) -> int:
        log = self._log.bind(operation="count")
        try:
            count = len(self._datamanager.get_data())
            log.info(f"Jumlah entities: {count}")
        except Exception as e:
            log.exception("Gagal count")
            raise RepositoryExcpError(f"{self.repo_name} gagal count") from e
        else:
            return count

    def clear(self):
        log = self._log.bind(operation="clear")
        try:
            self._datamanager.clear_data()
            log.info("Semua entities dihapus")
        except Exception as e:
            log.exception("Gagal clear")
            raise RepositoryExcpError(f"{self.repo_name} gagal clear") from e
