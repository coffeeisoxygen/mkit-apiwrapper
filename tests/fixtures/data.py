from pathlib import Path

import pytest
import yaml


@pytest.fixture(scope="session")
def test_file_path():
    return Path(__file__).parent.parent / "data"


@pytest.fixture(scope="session")
def valid_members_data(test_file_path):
    yaml_path = test_file_path / "members_valid.yaml"
    with open(yaml_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["members"]


@pytest.fixture(scope="session")
def valid_cities_data(test_file_path):
    yaml_path = test_file_path / "cities_valid.yaml"
    with open(yaml_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["cities"]
