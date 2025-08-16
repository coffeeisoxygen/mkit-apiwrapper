# app/core/svc_base.py
from typing import Any, TypeVar

from app.custom.exc_exceptions import ServiceExcpError
from app.mlogg import logger

T = TypeVar("T")  # entity type


class BaseService[T]:
    """Base service dengan fail-fast, contextual logging, dan ServiceExcpError."""

    service_name: str = "BaseService"  # override di subclass

    def __init__(self, repository: Any):
        self._repo = repository
        self._log = logger.bind(service=self.service_name)

    def add(self, key: str, entity: T):
        log = self._log.bind(operation="add", key=key)
        try:
            self._repo.add(key, entity)
            log.info("Entity ditambahkan lewat service")
        except Exception as e:
            log.exception("Service gagal add entity")
            raise ServiceExcpError(f"{self.service_name} gagal add") from e

    def get(self, key: str) -> T | None:
        log = self._log.bind(operation="get", key=key)
        try:
            entity = self._repo.get(key)
            if entity is None:
                log.warning("Entity tidak ditemukan via service")
            else:
                log.info("Entity ditemukan via service")
        except Exception as e:
            log.exception("Service gagal get entity")
            raise ServiceExcpError(f"{self.service_name} gagal get") from e
        else:
            return entity

    def delete(self, key: str):
        log = self._log.bind(operation="delete", key=key)
        try:
            self._repo.delete(key)
            log.info("Entity dihapus via service")
        except Exception as e:
            log.exception("Service gagal delete")
            raise ServiceExcpError(f"{self.service_name} gagal delete") from e

    def list_all(self) -> list[T]:
        log = self._log.bind(operation="list_all")
        try:
            entities = self._repo.get_all()
            log.info(f"Total entities: {len(entities)} via service")
        except Exception as e:
            log.exception("Service gagal list_all")
            raise ServiceExcpError(f"{self.service_name} gagal list_all") from e
        else:
            return entities
