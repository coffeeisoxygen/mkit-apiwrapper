from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.custom.utl_hasher import Hasher
from app.database.session import get_db_session
from app.services.member_service import MemberService


# factory buat Hasher (bisa reuse)
def get_hasher() -> Hasher:
    return Hasher()


# factory buat MemberService
def get_member_service(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    hasher: Annotated[Hasher, Depends(get_hasher)],
) -> MemberService:
    return MemberService(session, hasher)
