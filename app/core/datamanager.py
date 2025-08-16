from typing import Any, ClassVar, Self


class BaseDataManager:
    """Base class for managing data storage with singleton behavior per subclass.

    Provides methods to upload, retrieve, clear, add, and remove data items.
    """

    _instances: ClassVar[dict[type, Self]] = {}

    def _validate_key(self, key: str) -> None:
        """Helper to validate key is not None and is a string."""
        if key is None:
            raise TypeError("Key cannot be None")
        if not isinstance(key, str):
            raise TypeError("Key must be a string")

    def __new__(cls) -> Self:
        """Create or return a singleton instance for each subclass."""
        # Singleton per subclass
        if cls not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def __init__(self) -> None:
        """Initialize the data manager with an empty data dictionary if not already set."""
        if not hasattr(self, "_data"):
            self._data: dict[str, Any] = {}

    def upload_data(self, data: dict[str, Any]) -> None:
        """Update the internal data dictionary with the provided data.

        Args:
            data (dict[str, Any]): Data to upload.
        """
        self._data.update(data)

    def get_data(self) -> dict[str, Any]:
        """Get a copy of the internal data dictionary.

        Returns:
            dict[str, Any]: A copy of the stored data.
        """
        return dict(self._data)  # return copy biar lebih aman

    def clear_data(self) -> None:
        """Clear all data from the internal data dictionary."""
        self._data.clear()

    def get_item(self, key: str) -> Any:
        """Retrieve the value associated with the given key.

        Args:
            key (str): The key to look up.

        Returns:
            Any: The value associated with the key, or None if not found.
        """
        self._validate_key(key)
        return self._data.get(key)

    def add_item(self, key: str, value: Any) -> None:
        """Add a new item to the data dictionary.

        Args:
            key (str): The key for the item.
            value (Any): The value to store.

        Raises:
            ValueError: If the key already exists or is None.
            TypeError: If the key is not a string.
        """
        self._validate_key(key)
        if key in self._data:
            raise ValueError(f"Duplicate key: {key}")
        self._data[key] = value

    def remove_item(self, key: str) -> None:
        """Remove an item from the data dictionary by key.

        Args:
            key (str): The key of the item to remove.

        Raises:
            TypeError: If the key is not a string.
        """
        self._validate_key(key)
        self._data.pop(key, None)


# subclass
class MemberDataManager(BaseDataManager):
    """Data manager for member-related data."""

    pass


class ModuleDataManager(BaseDataManager):
    """Data manager for module-related data."""

    pass
