"""admin router for debuging data."""

from fastapi import APIRouter

from app.deps import DepAppSettings, DepMemberRepo, DepModuleRepo

router = APIRouter()


@router.get("/debug/members")
def debug_members(member_service: DepMemberRepo):
    return {"members": [m.model_dump() for m in member_service.get_all()]}


@router.get("/debug/modules")
def debug_modules(module_service: DepModuleRepo):
    return {"modules": [m.model_dump() for m in module_service.get_all()]}


@router.get("/debug/settings")
def debug_settings(app_settings: DepAppSettings):
    return app_settings
