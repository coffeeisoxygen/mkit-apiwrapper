from typing import Any, ClassVar, Self

from app.custom.exc_exceptions import DataManagerExcpError
from app.mlogg import logger


class BaseDataManager:
    """Base class fail-safe untuk manajemen data dengan singleton per subclass.

    Behavior:
    - CRUD operations log errors instead of raising exceptions
    - Singleton per subclass
    - Fatal errors (instance creation) tetap raise
    """

    _instances: ClassVar[dict[type, Self]] = {}

    def _validate_key(self, key: str) -> bool:
        log = logger.bind(operation="validate_key", key=key)
        if key is None:
            log.error("Key cannot be None")
            return False
        if not isinstance(key, str):
            log.error("Key must be a string")
            return False
        return True

    def __new__(cls) -> Self:
        """Singleton per subclass, fatal jika gagal."""
        log = logger.bind(operation="__new__", class_name=cls.__name__)
        if cls not in cls._instances:
            try:
                instance = super().__new__(cls)
                cls._instances[cls] = instance
                log.debug(f"DataManager instance created: {instance}")
            except DataManagerExcpError:
                log.exception("Failed to create DataManager instance")
                raise
        return cls._instances[cls]

    def __init__(self) -> None:
        """Init data dictionary jika belum ada."""
        if not hasattr(self, "_data"):
            self._data: dict[str, Any] = {}
            logger.bind(operation="__init__", class_name=self.__class__.__name__).info(
                "DataManager initialized"
            )

    def upload_data(self, data: dict[str, Any]) -> None:
        log = logger.bind(operation="upload_data", data=data)
        try:
            self._data.update(data)
            log.info("Data uploaded")
        except Exception:
            log.exception("Upload data failed")

    def get_data(self) -> dict[str, Any]:
        log = logger.bind(operation="get_data")
        try:
            result = dict(self._data)
            log.info("Data retrieved")
        except Exception:
            log.exception("Get data failed")
            return {}
        else:
            return result

    def clear_data(self) -> None:
        log = logger.bind(operation="clear_data")
        try:
            self._data.clear()
            log.info("Data cleared")
        except Exception:
            log.exception("Clear data failed")

    def get_item(self, key: str) -> Any:
        log = logger.bind(operation="get_item", key=key)
        if not self._validate_key(key):
            return None
        try:
            value = self._data.get(key)
            log.info(f"Item retrieved: {key} -> {value}")
        except Exception:
            log.exception("Get item failed")
            return None
        else:
            return value

    def add_item(self, key: str, value: Any) -> None:
        log = logger.bind(operation="add_item", key=key, value=value)
        if not self._validate_key(key):
            return
        if key in self._data:
            log.error(f"Duplicate key: {key}")
            return
        try:
            self._data[key] = value
            log.info(f"Item added: {key}")
        except Exception:
            log.exception("Add item failed")

    def remove_item(self, key: str) -> None:
        log = logger.bind(operation="remove_item", key=key)
        if not self._validate_key(key):
            return
        try:
            self._data.pop(key, None)
            log.info(f"Item removed: {key}")
        except Exception:
            log.exception("Remove item failed")
