from typing import Any, ClassVar, Self

from app.custom.exc_exceptions import DataManagerExcpError
from app.mlogg import logger


class BaseDataManager:
    """Base class for managing data storage with singleton behavior per subclass.

    Provides methods to upload, retrieve, clear, add, and remove data items.
    """

    _instances: ClassVar[dict[type, Self]] = {}

    def _validate_key(self, key: str) -> None:
        def _raise(exc: Exception):
            raise exc

        log = logger.bind(operation="validate_key", key=key)
        try:
            if key is None:
                log.error("Key cannot be None")
                _raise(TypeError("Key cannot be None"))
            if not isinstance(key, str):
                log.error("Key must be a string")
                _raise(TypeError("Key must be a string"))
        except Exception:
            log.exception("Validation failed")
            raise

    def __new__(cls) -> Self:
        """Create or return a singleton instance for each subclass."""
        log = logger.bind(operation="__new__", class_name=cls.__name__)
        try:
            if cls not in cls._instances:
                instance = super().__new__(cls)
                cls._instances[cls] = instance
            log.debug(f"DataManager instance created: {cls._instances[cls]}")
            return cls._instances[cls]
        except Exception:
            log.exception("Failed to create instance")
            raise

    def __init__(self) -> None:
        """Initialize the data manager with an empty data dictionary if not already set."""
        log = logger.bind(operation="__init__", class_name=self.__class__.__name__)
        try:
            if not hasattr(self, "_data"):
                self._data: dict[str, Any] = {}
        except Exception:
            log.exception("Initialization failed")
            raise

    def upload_data(self, data: dict[str, Any]) -> None:
        log = logger.bind(operation="upload_data", data=data)
        try:
            self._data.update(data)
            log.info("Data uploaded")
        except Exception as e:
            log.exception("Upload data failed")
            raise DataManagerExcpError("Failed to upload data") from e

    def get_data(self) -> dict[str, Any]:
        log = logger.bind(operation="get_data")
        try:
            result = dict(self._data)
            log.info("Data retrieved")
        except Exception as e:
            log.exception("Get data failed")
            raise DataManagerExcpError("Failed to get data") from e
        else:
            return result

    def clear_data(self) -> None:
        log = logger.bind(operation="clear_data")
        try:
            self._data.clear()
            log.info("Data cleared")
        except Exception as e:
            log.exception("Clear data failed")
            raise DataManagerExcpError("Failed to clear data") from e

    def get_item(self, key: str) -> Any:
        log = logger.bind(operation="get_item", key=key)
        try:
            self._validate_key(key)
            value = self._data.get(key)
            log.info(f"Item retrieved: {key} -> {value}")
        except Exception as e:
            log.exception("Get item failed")
            raise DataManagerExcpError(f"Failed to get item: {key}") from e
        else:
            return value

    def add_item(self, key: str, value: Any) -> None:
        log = logger.bind(operation="add_item", key=key, value=value)

        def _raise_duplicate_key(key: str):
            raise ValueError(f"Duplicate key: {key}")

        try:
            self._validate_key(key)
            if key in self._data:
                log.error(f"Duplicate key: {key}")
                _raise_duplicate_key(key)
            self._data[key] = value
            log.info(f"Item added: {key}")
        except Exception as e:
            log.exception("Add item failed")
            raise DataManagerExcpError(f"Failed to add item: {key}") from e

    def remove_item(self, key: str) -> None:
        log = logger.bind(operation="remove_item", key=key)
        try:
            self._validate_key(key)
            self._data.pop(key, None)
            log.info(f"Item removed: {key}")
        except Exception as e:
            log.exception("Remove item failed")
            raise DataManagerExcpError(f"Failed to remove item: {key}") from e


# subclass
class MemberDataManager(BaseDataManager):
    """Data manager for member-related data."""

    pass


class ModuleDataManager(BaseDataManager):
    """Data manager for module-related data."""

    pass
