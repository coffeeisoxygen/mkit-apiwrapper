import ipaddress

import pytest
from app.domain.member.sch_member import MemberInDB
from pydantic import ValidationError


def valid_member_dict():
    return {
        "memberid": "M12345",
        "name": "John Doe",
        "pin": "123456",
        "password": "password123",
        "ipaddress": "192.168.1.1",
        "report_url": "http://example.com/report",
        "is_active": True,
        "allow_nosign": False,
    }


def test_memberindb_valid():
    data = valid_member_dict()
    member = MemberInDB(**data)
    assert member.memberid == data["memberid"]
    assert member.name == data["name"]
    assert member.pin.get_secret_value() == data["pin"]
    assert member.password.get_secret_value() == data["password"]
    assert member.ip_address == ipaddress.IPv4Address(data["ipaddress"])
    assert str(member.report_url) == data["report_url"]
    assert member.is_active is True
    assert member.allow_nosign is False


@pytest.mark.parametrize(
    "field,value",
    [
        ("memberid", ""),  # too short
        ("name", ""),  # too short
        ("pin", ""),  # too short
        ("password", ""),  # too short
        ("ipaddress", "not_an_ip"),
        ("report_url", "not_a_url"),
    ],
)
def test_memberindb_invalid_fields(field, value):
    data = valid_member_dict()
    data[field] = value
    with pytest.raises(ValidationError):
        MemberInDB(**data)


def test_memberindb_missing_required():
    data = valid_member_dict()
    del data["memberid"]
    with pytest.raises(ValidationError):
        MemberInDB(**data)


def test_memberindb_pin_int_cast():
    data = valid_member_dict()
    data["pin"] = 123456
    member = MemberInDB(**data)
    assert member.pin.get_secret_value() == "123456"


def test_memberindb_password_int_cast():
    data = valid_member_dict()
    data["password"] = 987654
    member = MemberInDB(**data)
    assert member.password.get_secret_value() == "987654"


def test_memberindb_allow_nosign_default():
    data = valid_member_dict()
    del data["allow_nosign"]
    member = MemberInDB(**data)
    assert member.allow_nosign is False
