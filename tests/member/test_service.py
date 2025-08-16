"""
Unit tests for MemberService in app.domain.member.srv_member.

These tests cover member addition, bulk addition, existence checks, clearing,
duplicate key handling, and member deletion for the MemberService class.
"""

# pyright: reportUndefinedVariable=false, reportGeneralTypeIssues=false, reportArgumentType=false

import pytest
from app.custom.exc_exceptions import ServiceExcpError
from app.domain.member.sch_member import MemberInDB
from app.domain.member.srv_member import MemberService


def make_member(
    memberid="otomax1",
    name="Test",
    pin="123456",
    password="password",
    ipaddress="192.168.1.1",
    report_url="http://localhost/report",
    is_active=True,
    allow_nosign=False,
):
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


def test_add_and_get_member():
    service = MemberService()
    service._repo.clear()
    member = make_member("otomax1")
    service.add("otomax1", member)
    assert service.get("otomax1") == member


def test_add_bulk_and_count():
    service = MemberService()
    service._repo.clear()
    members = [make_member("otomax1"), make_member("OTOTEST")]
    service.add_bulk({m.memberid: m for m in members})
    assert service.count() == 2


def test_exists():
    service = MemberService()
    service._repo.clear()
    member = make_member("otomax1")
    service.add("otomax1", member)
    assert service.exists("otomax1") is True
    assert service.exists("missingid") is False


def test_clear():
    service = MemberService()
    service._repo.clear()
    members = [make_member("otomax1"), make_member("OTOTEST")]
    service.add_bulk({m.memberid: m for m in members})
    service._repo.clear()
    assert service.count() == 0


def test_add_duplicate_key_raises():
    service = MemberService()
    service._repo.clear()
    member = make_member("otomax1")
    service.add("otomax1", member)
    with pytest.raises(ServiceExcpError):
        service.add("otomax1", member)


def test_delete_member():
    service = MemberService()
    service._repo.clear()
    member = make_member("otomax1")
    service.add("otomax1", member)
    service.delete("otomax1")
    assert service.exists("otomax1") is False
