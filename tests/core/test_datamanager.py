"""
Unit tests for the DataManager classes in app.core.datamanager.

These tests cover singleton behavior, data upload/retrieval, item addition/removal,
subclass independence, error handling, and edge cases for BaseDataManager,
MemberDataManager, and ModuleDataManager.
"""

# pyright: reportUndefinedVariable=false, reportGeneralTypeIssues=false, reportArgumentType=false
import pytest
from app.core import BaseDataManager
from app.custom.exc_exceptions import DataManagerExcpError
from app.domain.member.dta_member import MemberDataManager
from app.domain.module.dta_module import ModuleDataManager


def test_singleton_behavior():
    """Test that MemberDataManager and ModuleDataManager implement singleton behavior."""
    a = MemberDataManager()
    b = MemberDataManager()
    c = ModuleDataManager()
    d = ModuleDataManager()
    assert a is b
    assert c is d
    assert a is not c


def test_upload_and_get_data():
    """Test uploading data and retrieving a copy from BaseDataManager."""
    mgr = BaseDataManager()
    mgr.clear_data()
    data = {"x": 1, "y": 2}
    mgr.upload_data(data)
    result = mgr.get_data()
    assert result == data
    # Ensure it's a copy
    result["x"] = 100
    assert mgr.get_data()["x"] == 1


def test_clear_data():
    """Test clearing all data from BaseDataManager."""
    mgr = BaseDataManager()
    mgr.upload_data({"a": 10})
    mgr.clear_data()
    assert mgr.get_data() == {}


def test_get_item():
    """Test retrieving an item by key from BaseDataManager."""
    mgr = BaseDataManager()
    mgr.clear_data()
    mgr.upload_data({"foo": "bar"})
    assert mgr.get_item("foo") == "bar"
    assert mgr.get_item("notfound") is None


def test_add_item_and_duplicate_key():
    """Test adding an item and handling duplicate keys in BaseDataManager."""
    mgr = BaseDataManager()
    mgr.clear_data()
    mgr.add_item("key1", "val1")
    assert mgr.get_item("key1") == "val1"
    with pytest.raises(DataManagerExcpError):
        mgr.add_item("key1", "val2")


def test_remove_item():
    """Test removing an item by key from BaseDataManager."""
    mgr = BaseDataManager()
    mgr.clear_data()
    mgr.upload_data({"a": 1, "b": 2})
    mgr.remove_item("a")
    assert "a" not in mgr.get_data()
    # Removing non-existent key should not raise
    mgr.remove_item("notfound")


def test_subclass_independence():
    """Test that MemberDataManager and ModuleDataManager maintain independent data."""
    member_mgr = MemberDataManager()
    module_mgr = ModuleDataManager()
    member_mgr.clear_data()
    module_mgr.clear_data()
    member_mgr.add_item("m", 123)
    module_mgr.add_item("mod", 456)
    assert member_mgr.get_item("m") == 123
    assert module_mgr.get_item("mod") == 456
    assert module_mgr.get_item("m") is None
    assert member_mgr.get_item("mod") is None


def test_upload_empty_data():
    """Test uploading empty data to BaseDataManager."""
    mgr = BaseDataManager()
    mgr.clear_data()
    mgr.upload_data({})
    assert mgr.get_data() == {}


def test_remove_item_from_empty():
    """Test removing an item from an empty BaseDataManager."""
    mgr = BaseDataManager()
    mgr.clear_data()
    mgr.remove_item("nonexistent")
    assert mgr.get_data() == {}


def test_add_none_key():
    """Test that adding an item with None as key raises an error."""
    mgr = BaseDataManager()
    mgr.clear_data()
    with pytest.raises(DataManagerExcpError):
        mgr.add_item(None, "value")


def test_add_empty_string_key():
    """Test adding and removing an item with an empty string key."""
    mgr = BaseDataManager()
    mgr.clear_data()
    mgr.add_item("", "empty")
    assert mgr.get_item("") == "empty"
    mgr.remove_item("")
    assert mgr.get_item("") is None


def test_large_data_upload():
    """Test uploading a large dataset to BaseDataManager."""
    mgr = BaseDataManager()
    mgr.clear_data()
    large_data = {str(i): i for i in range(1000)}
    mgr.upload_data(large_data)
    result = mgr.get_data()
    assert result == large_data


def test_remove_all_items_one_by_one():
    """Test removing all items from BaseDataManager one by one."""
    mgr = BaseDataManager()
    mgr.clear_data()
    data = {"a": 1, "b": 2, "c": 3}
    mgr.upload_data(data)
    for k in list(data.keys()):
        mgr.remove_item(k)
    assert mgr.get_data() == {}


def test_add_item_with_non_string_key():
    """Test that adding an item with a non-string key raises an error."""
    mgr = BaseDataManager()
    mgr.clear_data()
    with pytest.raises(DataManagerExcpError):
        mgr.add_item(123, "numberkey")


def test_get_item_with_non_string_key():
    """Test that getting an item with a non-string key raises an error."""
    mgr = BaseDataManager()
    mgr.clear_data()
    mgr.upload_data({"foo": "bar"})
    with pytest.raises(DataManagerExcpError):
        mgr.get_item(123)


def test_remove_item_with_non_string_key():
    """Test that removing an item with a non-string key raises an error."""
    mgr = BaseDataManager()
    mgr.clear_data()
    with pytest.raises(DataManagerExcpError):
        mgr.remove_item(123)
