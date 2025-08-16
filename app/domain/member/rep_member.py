from app.core import BaseRepository
from app.domain.member.dta_member import MemberDataManager
from app.domain.member.sch_member import MemberInDB


class MemberRepository(BaseRepository[MemberInDB]):
    repo_name = "MemberRepository"

    def __init__(self):
        super().__init__(datamanager=MemberDataManager())
