from pathlib import Path
from typing import Any

from app.domain.module.sch_module import ModuleInDB
from app.utils.loader.yaml_loader import YAMLDataImporter

KEYNAME = "modules"
IDFIELD = "moduleid"


class ModuleService:
    def __init__(self, yaml_path: Path, logger: Any):
        self.yaml_path = yaml_path
        self.logger = logger
        self._modules: list[ModuleInDB] = []

        # Loader setup (key_name di YAML harus "modules")
        self.loader = YAMLDataImporter(
            key_name=KEYNAME, id_field=IDFIELD, model=ModuleInDB, logger=logger
        )

    def load_modules(self) -> None:
        with self.logger.contextualize(
            module_count=len(self._modules), path=str(self.yaml_path)
        ):
            try:
                self._modules = self.loader.load_and_validate(self.yaml_path)
                self.logger.info(
                    f"✅ Loaded {len(self._modules)} modules from {self.yaml_path}"
                )
            except Exception as e:
                self.logger.error(f"❌ Failed to load modules: {e}")
                self.logger.info("Using previous module data in memory.")

    def get_all(self) -> list[ModuleInDB]:
        return self._modules

    def get_by_id(self, module_id: str) -> ModuleInDB | None:
        return next((m for m in self._modules if m.moduleid == module_id), None)

    def is_active(self, module_id: str) -> bool:
        module = self.get_by_id(module_id)
        return bool(module and module.is_active)
