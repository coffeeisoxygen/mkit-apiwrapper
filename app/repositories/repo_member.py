from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base_crud import AppCRUD
from app.models.member import Member
from app.repositories.intf_member import IMemberRepository


class MemberRepository(AppCRUD, IMemberRepository):
    """Implementasi repository untuk Member."""

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, member: Member) -> Member:
        self.session.add(member)
        return await self.commit_refresh(member)

    async def get_by_id(self, member_id: str) -> Member | None:
        result = await self.session.execute(
            select(Member).where(Member.memberid == member_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> Sequence[Member]:
        result = await self.session.execute(select(Member))
        return result.scalars().all()

    async def update(self, member: Member) -> Member:
        """Karena sudah terikat ke session, tinggal commit_refresh."""
        return await self.commit_refresh(member)

    async def delete(self, member: Member) -> None:
        await self.session.delete(member)
        await self.commit()
