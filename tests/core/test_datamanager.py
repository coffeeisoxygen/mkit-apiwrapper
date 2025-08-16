import pytest
from app.core.datamanager import BaseDataManager, MemberDataManager, ModuleDataManager


def test_singleton_behavior():
    a = MemberDataManager()
    b = MemberDataManager()
    c = ModuleDataManager()
    d = ModuleDataManager()
    assert a is b
    assert c is d
    assert a is not c


def test_upload_and_get_data():
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
    mgr = BaseDataManager()
    mgr.upload_data({"a": 10})
    mgr.clear_data()
    assert mgr.get_data() == {}


def test_get_item():
    mgr = BaseDataManager()
    mgr.clear_data()
    mgr.upload_data({"foo": "bar"})
    assert mgr.get_item("foo") == "bar"
    assert mgr.get_item("notfound") is None


def test_add_item_and_duplicate_key():
    mgr = BaseDataManager()
    mgr.clear_data()
    mgr.add_item("key1", "val1")
    assert mgr.get_item("key1") == "val1"
    with pytest.raises(ValueError):
        mgr.add_item("key1", "val2")


def test_remove_item():
    mgr = BaseDataManager()
    mgr.clear_data()
    mgr.upload_data({"a": 1, "b": 2})
    mgr.remove_item("a")
    assert "a" not in mgr.get_data()
    # Removing non-existent key should not raise
    mgr.remove_item("notfound")


def test_subclass_independence():
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
    mgr = BaseDataManager()
    mgr.clear_data()
    mgr.upload_data({})
    assert mgr.get_data() == {}


def test_remove_item_from_empty():
    mgr = BaseDataManager()
    mgr.clear_data()
    mgr.remove_item("nonexistent")
    assert mgr.get_data() == {}


def test_add_none_key():
    mgr = BaseDataManager()
    mgr.clear_data()
    with pytest.raises(TypeError):
        mgr.add_item(None, "value")  # pyright: ignore[reportArgumentType]


def test_add_empty_string_key():
    mgr = BaseDataManager()
    mgr.clear_data()
    mgr.add_item("", "empty")
    assert mgr.get_item("") == "empty"
    mgr.remove_item("")
    assert mgr.get_item("") is None


def test_large_data_upload():
    mgr = BaseDataManager()
    mgr.clear_data()
    large_data = {str(i): i for i in range(1000)}
    mgr.upload_data(large_data)
    result = mgr.get_data()
    assert result == large_data


def test_remove_all_items_one_by_one():
    mgr = BaseDataManager()
    mgr.clear_data()
    data = {"a": 1, "b": 2, "c": 3}
    mgr.upload_data(data)
    for k in list(data.keys()):
        mgr.remove_item(k)
    assert mgr.get_data() == {}


def test_add_item_with_non_string_key():
    mgr = BaseDataManager()
    mgr.clear_data()
    with pytest.raises(TypeError):
        mgr.add_item(123, "numberkey")  # type: ignore


def test_get_item_with_non_string_key():
    mgr = BaseDataManager()
    mgr.clear_data()
    mgr.upload_data({"foo": "bar"})
    with pytest.raises(TypeError):
        mgr.get_item(123)  # type: ignore


def test_remove_item_with_non_string_key():
    mgr = BaseDataManager()
    mgr.clear_data()
    with pytest.raises(TypeError):
        mgr.remove_item(123)
