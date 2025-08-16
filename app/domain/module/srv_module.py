from app.core import BaseService
from app.custom.exc_exceptions import ServiceExcpError
from app.domain.module.rep_module import ModuleRepository
from app.domain.module.sch_module import ModuleInDB


class ModuleService(BaseService[ModuleInDB]):
    service_name = "ModuleService"

    def __init__(self):
        super().__init__(repository=ModuleRepository())

    def add_bulk(self, items: dict[str, ModuleInDB]):
        log = self._log.bind(operation="add_bulk", count=len(items))
        try:
            for key, entity in items.items():
                self.add(key, entity)  # fail-fast per item
            log.info("Bulk modules ditambahkan via service")
        except Exception as e:
            log.exception("Service gagal add_bulk")
            raise ServiceExcpError(f"{self.service_name} gagal add_bulk") from e

    def exists(self, key: str) -> bool:
        log = self._log.bind(operation="exists", key=key)
        try:
            exists = self._repo.exists(key)
            log.info(f"Exists: {exists} via service")
        except Exception as e:
            log.exception("Service gagal exists")
            raise ServiceExcpError(f"{self.service_name} gagal exists") from e
        else:
            return exists

    def count(self) -> int:
        log = self._log.bind(operation="count")
        try:
            count = self._repo.count()
            log.info(f"Jumlah modules: {count} via service")
        except Exception as e:
            log.exception("Service gagal count")
            raise ServiceExcpError(f"{self.service_name} gagal count") from e
        else:
            return count
