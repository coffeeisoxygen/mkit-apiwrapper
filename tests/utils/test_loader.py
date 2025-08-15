from pathlib import Path

import pytest
from app.custom.exc_exceptions import FileLoaderExcpError
from app.utils.loader.yaml_loader import YAMLDataImporter
from pydantic import BaseModel


class DummyModel(BaseModel):
    memberid: str
    name: str


class DummyLogger:
    def __init__(self):
        self.messages = []

    def info(self, msg):
        self.messages.append(msg)


@pytest.fixture
def dummy_logger():
    return DummyLogger()


def test_load_and_validate_success(test_file_path, dummy_logger):
    yaml_path = test_file_path / "members_valid.yaml"
    importer = YAMLDataImporter(
        key_name="members",
        id_field="memberid",
        model=DummyModel,
        logger=dummy_logger,
    )
    items = importer.load_and_validate(yaml_path)
    assert len(items) == 2
    assert items[0].memberid == "otomax1"
    assert items[1].memberid == "OTOTEST"
    assert "Loaded 2 members" in dummy_logger.messages[0]


def test_file_not_found(dummy_logger):
    importer = YAMLDataImporter(
        key_name="members",
        id_field="memberid",
        model=DummyModel,
        logger=dummy_logger,
    )
    with pytest.raises(FileLoaderExcpError, match="YAML file not found"):
        importer.load_and_validate(Path("nonexistent.yaml"))


def test_missing_key(test_file_path, dummy_logger):
    yaml_path = test_file_path / "members_missing_key.yaml"
    importer = YAMLDataImporter(
        key_name="members",
        id_field="memberid",
        model=DummyModel,
        logger=dummy_logger,
    )
    with pytest.raises(FileLoaderExcpError, match="must contain 'members' key"):
        importer.load_and_validate(yaml_path)


def test_duplicate_id(test_file_path, dummy_logger):
    yaml_path = test_file_path / "members_duplicate.yaml"
    importer = YAMLDataImporter(
        key_name="members",
        id_field="memberid",
        model=DummyModel,
        logger=dummy_logger,
    )
    with pytest.raises(FileLoaderExcpError, match="Duplicate memberids found"):
        importer.load_and_validate(yaml_path)


def test_validation_error(test_file_path, dummy_logger):
    yaml_path = test_file_path / "members_invalid.yaml"
    importer = YAMLDataImporter(
        key_name="members",
        id_field="memberid",
        model=DummyModel,
        logger=dummy_logger,
    )
    with pytest.raises(FileLoaderExcpError, match="Validation failed at index"):
        importer.load_and_validate(yaml_path)
