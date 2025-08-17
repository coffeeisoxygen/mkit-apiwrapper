from sqlalchemy.ext.asyncio import AsyncSession

from app.custom.utl_hasher import Hasher
from app.repository.member_repo import MemberRepository
from app.schemas.member.member_crud import MemberCreate, MemberRead


class MemberService:
    def __init__(self, session: AsyncSession, hasher: Hasher):
        self.repo = MemberRepository(session)
        self.hasher = hasher

    async def register_member(self, data: MemberCreate) -> MemberRead:
        # Check for duplicate memberid
        existing_member = await self.repo.get_by_id(data.memberid)
        if existing_member:
            raise ValueError(f"Member with memberid '{data.memberid}' already exists.")

        hashed_password = self.hasher.hash(data.hash_password.get_secret_value())
        hashed_pin = self.hasher.hash(data.hash_pin.get_secret_value())

        new_member = await self.repo.create({
            "memberid": data.memberid,
            "name": data.name,
            "ip_address": data.ipaddress,
            "report_url": data.report_url,
            "hash_pin": hashed_pin,
            "hash_password": hashed_password,
        })
        return MemberRead.model_validate(new_member)

    async def get_member(self, member_id: str) -> MemberRead | None:
        member = await self.repo.get_by_id(member_id)
        return MemberRead.model_validate(member) if member else None
