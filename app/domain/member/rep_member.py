from app.domain.member.sch_member import MemberInDB


class MemberRepository:
    def __init__(self):
        self._members: dict[str, MemberInDB] = {}

    def load(self, members: list[MemberInDB]):
        self._members = {m.memberid: m for m in members}

    def get(self, memberid: str) -> MemberInDB | None:
        return self._members.get(memberid)

    def all(self) -> list[MemberInDB]:
        return list(self._members.values())

    def count(self) -> int:
        return len(self._members)

    def exists(self, memberid: str) -> bool:
        return memberid in self._members

    def clear(self):
        self._members.clear()
