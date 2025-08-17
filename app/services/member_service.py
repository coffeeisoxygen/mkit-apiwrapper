from sqlalchemy.ext.asyncio import AsyncSession

from app.custom.utl_hasher import Hasher
from app.models.member import Member
from app.repositories import IMemberRepository, MemberRepository
from app.schemas.member.member_crud import MemberCreate, MemberRead


class MemberService:
    def __init__(self, session: AsyncSession, hasher: Hasher):
        # disini injeksi session + infra lain
        self.repo: IMemberRepository = MemberRepository(session)
        self.hasher = hasher

    async def register_member(self, data: MemberCreate) -> MemberRead:
        # cek duplikat memberid
        existing = await self.repo.get_by_id(data.memberid)
        if existing:
            raise ValueError(f"Member '{data.memberid}' already exists.")

        # bikin entity Member (langsung model db)
        new_member = Member(
            memberid=data.memberid,
            name=data.name,
            ipaddress=data.ipaddress,
            report_url=data.report_url,
            hash_pin=self.hasher.hash(data.pin.get_secret_value()),
            hash_password=self.hasher.hash(data.password.get_secret_value()),
        )

        saved = await self.repo.create(new_member)
        return MemberRead.model_validate(saved)

    async def get_member(self, member_id: str) -> MemberRead | None:
        member = await self.repo.get_by_id(member_id)
        return MemberRead.model_validate(member) if member else None

    async def list_members(self) -> list[MemberRead]:
        members = await self.repo.get_all()
        return [MemberRead.model_validate(m) for m in members]

    async def update_member(self, member_id: str, data: dict) -> MemberRead | None:
        member = await self.repo.get_by_id(member_id)
        if not member:
            return None

        # apply perubahan (exclude field sensitif)
        for k, v in data.items():
            if hasattr(member, k) and k not in ["memberid", "created_at", "updated_at"]:
                setattr(member, k, v)

        updated = await self.repo.update(member)
        return MemberRead.model_validate(updated)

    async def delete_member(self, member_id: str) -> bool:
        member = await self.repo.get_by_id(member_id)
        if not member:
            return False
        await self.repo.delete(member)
        return True
