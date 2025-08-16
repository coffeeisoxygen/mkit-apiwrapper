from fastapi import APIRouter

from app.deps import DepModuleRepo

router = APIRouter()


@router.get("/modules")
def get_modules(module_repo: DepModuleRepo):
    return {"modules": [m.model_dump() for m in module_repo.get_all()]}


@router.get("/modules/{moduleid}")
def get_module(moduleid: str, module_repo: DepModuleRepo):
    module = module_repo.get(moduleid)
    if module:
        return module.model_dump()
    return {"error": "Module not found"}


@router.post("/modules")
def create_module(module: dict, module_repo: DepModuleRepo):
    key = module.get("moduleid")
    module_repo.add(key, module)
    return {"message": "Module created", "moduleid": key}


@router.put("/modules/{moduleid}")
def update_module(moduleid: str, module: dict, module_repo: DepModuleRepo):
    module_repo.update(moduleid, module)
    return {"message": "Module updated", "moduleid": moduleid}


@router.delete("/modules/{moduleid}")
def delete_module(moduleid: str, module_repo: DepModuleRepo):
    module_repo.delete(moduleid)
    return {"message": "Module deleted", "moduleid": moduleid}
