from pathlib import Path

import pytest
from app.domain.member.sch_member import MemberInDB
from app.domain.member.srv_member import MemberService


class DummyLogger:
    def __init__(self):
        self.messages = []

    def info(self, msg):
        self.messages.append(msg)

    def error(self, msg):
        self.messages.append(msg)


@pytest.fixture
def dummy_logger():
    return DummyLogger()


@pytest.fixture
def valid_yaml_path():
    return Path("tests/data/members_valid.yaml")


def test_load_members_success(valid_yaml_path, dummy_logger):
    service = MemberService(valid_yaml_path, dummy_logger)
    service.load_members()
    members = service.get_all()
    assert len(members) == 2
    assert isinstance(members[0], MemberInDB)
    assert members[0].memberid == "otomax1"
    assert members[1].memberid == "OTOTEST"


def test_get_by_id(valid_yaml_path, dummy_logger):
    service = MemberService(valid_yaml_path, dummy_logger)
    service.load_members()
    member = service.get_by_id("otomax1")
    assert member is not None
    assert member.name == "otomax utama untuk testing dengan sign"


def test_is_active(valid_yaml_path, dummy_logger):
    service = MemberService(valid_yaml_path, dummy_logger)
    service.load_members()
    assert service.is_active("otomax1") is True
    assert service.is_active("OTOTEST") is True


def test_missing_file(dummy_logger):
    service = MemberService(Path("tests/data/notfound.yaml"), dummy_logger)
    with pytest.raises(Exception):  # noqa: B017
        service.load_members()
