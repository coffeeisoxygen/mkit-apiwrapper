"""admin router for debuging data."""

from fastapi import APIRouter

from app.deps import DepMemberService, DepModuleService

router = APIRouter()


@router.get("/debug/members", tags=["Debug"])
def debug_members(member_service: DepMemberService):
    return {"members": [m.model_dump() for m in member_service.get_all()]}


@router.get("/debug/modules", tags=["Debug"])
def debug_modules(module_service: DepModuleService):
    return {"modules": [m.model_dump() for m in module_service.get_all()]}
