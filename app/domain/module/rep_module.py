from app.core import BaseRepository
from app.domain.module.dta_module import ModuleDataManager
from app.domain.module.sch_module import ModuleInDB


class ModuleRepository(BaseRepository[ModuleInDB]):
    repo_name = "ModuleRepository"

    def __init__(self):
        super().__init__(datamanager=ModuleDataManager())
