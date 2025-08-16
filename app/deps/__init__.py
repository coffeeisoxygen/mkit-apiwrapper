"""dependencies untuk aplikasi di simpan dsini , biar lebih terstruktur dan mudah di kelola."""

from typing import Annotated

from fastapi import Depends, Request

from app.core.orchestrator import ModuleService
from app.domain.member.srv_member import MemberService


def get_member_service(request: Request) -> MemberService:
    return request.app.state.orchestrator.get_member_service()


DepMemberService = Annotated[MemberService, Depends(get_member_service)]


def get_module_service(request: Request) -> ModuleService:
    return request.app.state.orchestrator.get_module_service()


DepModuleService = Annotated[ModuleService, Depends(get_module_service)]
