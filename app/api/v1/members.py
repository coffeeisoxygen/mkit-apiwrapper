from fastapi import APIRouter

from app.deps import DepMemberRepo
from app.domain.member.sch_member import MemberInDB

router = APIRouter()


@router.get("/members")
def get_members(member_repo: DepMemberRepo):
    return {"members": [m.model_dump() for m in member_repo.get_all()]}


@router.get("/members/{memberid}")
def get_member(memberid: str, member_repo: DepMemberRepo):
    member = member_repo.get(memberid)
    if member:
        return member.model_dump()
    return {"error": "Member not found"}


@router.post("/members")
def create_member(member: dict, member_repo: DepMemberRepo):
    """Create a new member.

    Parameters
    ----------
    member : dict
        Member data as a dictionary.
    member_repo : DepMemberRepo
        Dependency-injected member repository.

    Returns:
    -------
    dict
        Result message and member ID, or error if input is invalid.
    """
    key = member.get("memberid")
    if not key:
        return {"error": "Missing memberid in request body"}
    try:
        member_obj = MemberInDB(**member)
    except Exception as exc:
        return {"error": f"Invalid member data: {exc}"}
    member_repo.add(key, member_obj)
    return {"message": "Member created", "memberid": key}


@router.put("/members/{memberid}")
def update_member(memberid: str, member: dict, member_repo: DepMemberRepo):
    """Update an existing member.

    Parameters
    ----------
    memberid : str
        ID of the member to update.
    member : dict
        Updated member data as a dictionary.
    member_repo : DepMemberRepo
        Dependency-injected member repository.

    Returns:
    -------
    dict
        Result message and member ID, or error if input is invalid.
    """
    try:
        member_obj = MemberInDB(**member)
    except Exception as exc:
        return {"error": f"Invalid member data: {exc}"}
    member_repo.update(memberid, member_obj)
    return {"message": "Member updated", "memberid": memberid}


@router.delete("/members/{memberid}")
def delete_member(memberid: str, member_repo: DepMemberRepo):
    member_repo.delete(memberid)
    return {"message": "Member deleted", "memberid": memberid}
