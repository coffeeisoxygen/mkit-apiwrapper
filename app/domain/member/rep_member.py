from app.core.datamanager import MemberDataManager
from app.domain.member.sch_member import MemberInDB


class MemberRepository:
    def __init__(self):
        self._datamanager = MemberDataManager()

    def load(self, members: list[MemberInDB]):
        # Simpan ke datamanager
        self._datamanager.upload_data({m.memberid: m for m in members})

    def get(self, memberid: str) -> MemberInDB | None:
        return self._datamanager.get_item(memberid)

    def all(self) -> list[MemberInDB]:
        return list(self._datamanager.get_data().values())

    def count(self) -> int:
        return len(self._datamanager.get_data())

    def exists(self, memberid: str) -> bool:
        return memberid in self._datamanager.get_data()

    def clear(self):
        self._datamanager.clear_data()
