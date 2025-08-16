"""dependencies untuk aplikasi di simpan dsini , biar lebih terstruktur dan mudah di kelola."""

from typing import Annotated

from fastapi import Depends, Request

from app.config import get_settings
from app.domain.member.rep_member import MemberRepository
from app.domain.module.rep_module import ModuleRepository

settings = get_settings()


def get_app_settings(request: Request):
    return {"settings": settings.model_dump()}


DepAppSettings = Annotated[dict, Depends(get_app_settings)]


def get_member_repo(request: Request) -> MemberRepository:
    return request.app.state.orchestrator.get_member_repo()


DepMemberRepo = Annotated[MemberRepository, Depends(get_member_repo)]


def get_module_repo(request: Request) -> ModuleRepository:
    return request.app.state.orchestrator.get_module_repo()


DepModuleRepo = Annotated[ModuleRepository, Depends(get_module_repo)]
