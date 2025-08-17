from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.deps.dep_members import get_member_service
from app.schemas.member.member_crud import MemberCreate, MemberRead
from app.services.member_service import MemberService

router = APIRouter(prefix="/members", tags=["Members"])


@router.post("/", response_model=MemberRead, status_code=status.HTTP_201_CREATED)
async def register_member(
    data: MemberCreate,
    service: Annotated[MemberService, Depends(get_member_service)],
):
    try:
        return await service.register_member(data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{member_id}", response_model=MemberRead)
async def get_member(
    member_id: str,
    service: Annotated[MemberService, Depends(get_member_service)],
):
    member = await service.get_member(member_id)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Member not found"
        )
    return member


@router.get("/", response_model=list[MemberRead])
async def list_members(
    service: Annotated[MemberService, Depends(get_member_service)],
):
    return await service.list_members()
