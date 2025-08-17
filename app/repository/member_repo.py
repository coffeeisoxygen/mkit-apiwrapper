# member_repo.py
from sqlalchemy import select

from app.models.member import Member
from app.repository.base_crud import AppCRUD
from app.repository.intf_member import IMemberRepository


class MemberRepository(AppCRUD, IMemberRepository):
    async def create(self, member_data: dict) -> Member:
        member = Member(**member_data)
        self.session.add(member)
        return await self.commit_refresh(member)

    async def get_by_id(self, member_id: str) -> Member | None:
        result = await self.session.execute(
            select(Member).where(Member.memberid == member_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Member]:
        result = await self.session.execute(select(Member))
        return list(result.scalars().all())

    async def update(self, member_id: str, member_data: dict) -> Member | None:
        member = await self.get_by_id(member_id)
        if not member:
            return None
        for k, v in member_data.items():
            if hasattr(member, k) and k not in ["memberid", "created_at", "updated_at"]:
                setattr(member, k, v)
        return await self.commit_refresh(member)

    async def delete(self, member_id: str) -> bool:
        member = await self.get_by_id(member_id)
        if not member:
            return False
        await self.session.delete(member)
        await self.commit()
        return True
