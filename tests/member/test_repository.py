import pytest
from app.domain.member.rep_member import MemberRepository
from app.domain.member.sch_member import MemberInDB


def make_member(
    memberid="otomax1",
    name="Test",
    pin="123456",  # <-- Changed to 6 characters
    password="password",
    ipaddress="192.168.1.1",
    report_url="http://localhost/report",
    is_active=True,
    allow_nosign=False,
):
    # Minimal MemberInDB stub for testing, with all required fields
    return MemberInDB(
        memberid=memberid,
        name=name,
        pin=pin,
        password=password,
        ipaddress=ipaddress,
        report_url=report_url,
        is_active=is_active,
        allow_nosign=allow_nosign,
    )


def make_member_from_dict(data):
    # Helper to create MemberInDB from dict loaded from YAML
    # Fill missing required fields with defaults
    defaults = {
        "name": "Test",
        "pin": "123456",
        "password": "password",
        "ipaddress": "192.168.1.1",
        "report_url": "http://localhost/report",
        "is_active": True,
        "allow_nosign": False,
    }
    member_data = {
        **defaults,
        **{k: v for k, v in data.items() if k in MemberInDB.__fields__},
    }
    return MemberInDB(**member_data)


@pytest.mark.usefixtures("valid_members_data")
def test_load_and_get_member(valid_members_data):
    repo = MemberRepository()
    member = make_member_from_dict(valid_members_data[0])
    repo.load([member])
    assert repo.get(member.memberid) == member


@pytest.mark.usefixtures("valid_members_data")
def test_all_returns_all_members(valid_members_data):
    repo = MemberRepository()
    members = [make_member_from_dict(m) for m in valid_members_data]
    repo.load(members)
    assert set(repo.all()) == set(members)


@pytest.mark.usefixtures("valid_members_data")
def test_count_returns_number_of_members(valid_members_data):
    repo = MemberRepository()
    members = [make_member_from_dict(m) for m in valid_members_data]
    repo.load(members)
    assert repo.count() == len(members)


@pytest.mark.usefixtures("valid_members_data")
def test_exists_checks_member_existence(valid_members_data):
    repo = MemberRepository()
    member = make_member_from_dict(valid_members_data[0])
    repo.load([member])
    assert repo.exists(member.memberid)
    assert not repo.exists("missingid")


def test_clear_removes_all_members():
    repo = MemberRepository()
    repo.load([make_member("otomax1"), make_member("OTOTEST")])
    repo.clear()
    assert repo.count() == 0
    assert repo.all() == []
