from app.core.datamanager import MemberDataManager
from app.domain.member.sch_member import MemberInDB


class MemberRepository:
    def __init__(self):
        self._datamanager = MemberDataManager()

    def add_member(self, member: MemberInDB):
        self._datamanager.add_item(member.memberid, member)

    def add_bulk_members(self, members: list[MemberInDB]):
        for member in members:
            self.add_member(member)

    def delete_member(self, memberid: str):
        self._datamanager.remove_item(memberid)

    def get_member(self, memberid: str) -> MemberInDB | None:
        return self._datamanager.get_item(memberid)

    def get_all_members(self) -> list[MemberInDB]:
        return list(self._datamanager.get_data().values())

    def count_members(self) -> int:
        return len(self._datamanager.get_data())

    def exists(self, memberid: str) -> bool:
        return memberid in self._datamanager.get_data()

    def clear(self):
        self._datamanager.clear_data()
