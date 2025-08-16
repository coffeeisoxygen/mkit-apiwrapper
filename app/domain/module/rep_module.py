from app.domain.module.sch_module import ModuleInDB


class ModuleRepository:
    def __init__(self):
        self._modules: dict[str, ModuleInDB] = {}

    def load(self, modules: list[ModuleInDB]):
        self._modules = {m.moduleid: m for m in modules}

    def get(self, moduleid: str) -> ModuleInDB | None:
        return self._modules.get(moduleid)

    def all(self) -> list[ModuleInDB]:
        return list(self._modules.values())

    def count(self) -> int:
        return len(self._modules)

    def exists(self, moduleid: str) -> bool:
        return moduleid in self._modules

    def clear(self):
        self._modules.clear()
