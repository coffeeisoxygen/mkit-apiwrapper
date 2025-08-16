"""admin router for debuging data."""

from fastapi import APIRouter

from app.deps import DepAppSettings, DepMemberService, DepModuleService

router = APIRouter()


@router.get("/debug/members")
def debug_members(member_service: DepMemberService):
    return {"members": [m.model_dump() for m in member_service.get_all()]}


@router.get("/debug/modules")
def debug_modules(module_service: DepModuleService):
    return {"modules": [m.model_dump() for m in module_service.get_all()]}


@router.get("/debug/settings")
def debug_settings(app_settings: DepAppSettings):
    return app_settings
