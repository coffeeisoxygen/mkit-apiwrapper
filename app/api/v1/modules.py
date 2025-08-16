from fastapi import APIRouter

from app.deps import DepModuleRepo
from app.domain.module.sch_module import ModuleInDB  # Assumed import

router = APIRouter()


@router.get("/modules")
def get_modules(module_repo: DepModuleRepo):
    """Get a list of all modules.

    Parameters
    ----------
    module_repo : DepModuleRepo
        Dependency-injected module repository.

    Returns:
    -------
    dict
        Dictionary containing a list of modules.
    """
    return {"modules": [m.model_dump() for m in module_repo.get_all()]}


@router.get("/modules/{moduleid}")
def get_module(moduleid: str, module_repo: DepModuleRepo):
    """Get a module by its ID.

    Parameters
    ----------
    moduleid : str
        ID of the module to retrieve.
    module_repo : DepModuleRepo
        Dependency-injected module repository.

    Returns:
    -------
    dict
        Module data or error message.
    """
    module = module_repo.get(moduleid)
    if module:
        return module.model_dump()
    return {"error": "Module not found"}


@router.post("/modules")
def create_module(module: dict, module_repo: DepModuleRepo):
    """Create a new module.

    Parameters
    ----------
    module : dict
        Module data as a dictionary.
    module_repo : DepModuleRepo
        Dependency-injected module repository.

    Returns:
    -------
    dict
        Result message and module ID, or error if input is invalid.
    """
    key = module.get("moduleid")
    if not key or not isinstance(key, str):
        return {"error": "Missing or invalid moduleid in request body"}
    try:
        module_obj = ModuleInDB(**module)
    except Exception as exc:
        return {"error": f"Invalid module data: {exc}"}
    module_repo.add(key, module_obj)
    return {"message": "Module created", "moduleid": key}


@router.put("/modules/{moduleid}")
def update_module(moduleid: str, module: dict, module_repo: DepModuleRepo):
    """Update an existing module.

    Parameters
    ----------
    moduleid : str
        ID of the module to update.
    module : dict
        Updated module data as a dictionary.
    module_repo : DepModuleRepo
        Dependency-injected module repository.

    Returns:
    -------
    dict
        Result message and module ID, or error if input is invalid.
    """
    try:
        module_obj = ModuleInDB(**module)
    except Exception as exc:
        return {"error": f"Invalid module data: {exc}"}
    module_repo.update(moduleid, module_obj)
    return {"message": "Module updated", "moduleid": moduleid}


@router.delete("/modules/{moduleid}")
def delete_module(moduleid: str, module_repo: DepModuleRepo):
    """Delete a module by its ID.

    Parameters
    ----------
    moduleid : str
        ID of the module to delete.
    module_repo : DepModuleRepo
        Dependency-injected module repository.

    Returns:
    -------
    dict
        Result message and module ID.
    """
    module_repo.delete(moduleid)
    return {"message": "Module deleted", "moduleid": moduleid}
