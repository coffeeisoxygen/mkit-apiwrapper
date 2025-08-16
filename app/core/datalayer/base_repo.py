from typing import Any, TypeVar

from app.mlogg import logger

T = TypeVar("T")  # entity type


class BaseRepository[T]:
    """BaseRepository provides CRUD operations with fail-safe logging for entities.

    Args:
        datamanager (Any): The data manager instance responsible for data storage operations.

    Attributes:
        repo_name (str): Name of the repository, used for logging.
    """

    repo_name: str = "BaseRepository"

    def __init__(self, datamanager: Any):
        """Initialize the repository with a data manager.

        Args:
            datamanager (Any): The data manager instance.
        """
        self._datamanager = datamanager
        self._log = logger.bind(repo=self.repo_name)

    def add(self, key: str, entity: T):
        """Add a new entity to the data manager.

        Args:
            key (str): The key for the entity.
            entity (T): The entity to add.
        """
        log = self._log.bind(operation="add", key=key)
        try:
            self._datamanager.add_item(key, entity)
            log.info("Entity ditambahkan")
        except Exception:
            log.exception("Gagal add entity")

    def get(self, key: str) -> T | None:
        """Retrieve an entity by key.

        Args:
            key (str): The key of the entity.

        Returns:
            T | None: The entity if found, otherwise None.
        """
        log = self._log.bind(operation="get", key=key)
        try:
            entity = self._datamanager.get_item(key)
        except Exception:
            log.exception("Gagal get entity")
            return None
        else:
            log.info(
                "Entity ditemukan" if entity is not None else "Entity tidak ditemukan"
            )
            return entity

    def get_all(self) -> list[T]:
        """Retrieve all entities from the data manager.

        Returns:
            list[T]: List of all entities.
        """
        log = self._log.bind(operation="get_all")
        try:
            entities = list(self._datamanager.get_data().values())
        except Exception:
            log.exception("Gagal get_all")
            return []
        else:
            log.info(f"Total entities: {len(entities)}")
            return entities

    def delete(self, key: str):
        """Delete an entity by key.

        Args:
            key (str): The key of the entity to delete.
        """
        log = self._log.bind(operation="delete", key=key)
        try:
            self._datamanager.remove_item(key)
            log.info("Entity dihapus")
        except Exception:
            log.exception("Gagal delete")

    def clear(self):
        """Remove all entities from the data manager."""
        log = self._log.bind(operation="clear")
        try:
            self._datamanager.clear_data()
            log.info("Semua entities dihapus")
        except Exception:
            log.exception("Gagal clear")

    def update(self, key: str, entity: T):
        """Update an existing entity by key.

        Args:
            key (str): The key of the entity to update.
            entity (T): The updated entity.
        """
        log = self._log.bind(operation="update", key=key)
        try:
            if key in self._datamanager.get_data():
                self._datamanager._data[key] = entity
                log.info("Entity diupdate")
            else:
                log.warning("Entity tidak ditemukan untuk update")
        except Exception:
            log.exception("Gagal update entity")

    def upsert(self, key: str, entity: T):
        """Add or update an entity by key.

        Args:
            key (str): The key of the entity.
            entity (T): The entity to add or update.
        """
        log = self._log.bind(operation="upsert", key=key)
        try:
            if key in self._datamanager.get_data():
                self.update(key, entity)
                log.info("Entity diupdate (upsert)")
            else:
                self.add(key, entity)
                log.info("Entity baru ditambahkan (upsert)")
        except Exception:
            log.exception("Gagal upsert entity")
