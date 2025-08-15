from pathlib import Path
from typing import Any, TypeVar

import yaml
import yaml.error
from app.custom.exc_exceptions import FileLoaderExcpError
from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)


class YAMLDataImporter[T: BaseModel]:
    def _check_file_exists(self, yaml_path: Path):
        if not yaml_path.exists():
            self.logger.error(f"YAML file not found: {yaml_path}")
            raise FileLoaderExcpError(f"YAML file not found: {yaml_path}")

    def _parse_yaml(self, yaml_path: Path):
        try:
            with yaml_path.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except yaml.error as e:
            self.logger.error(f"Failed to parse YAML file: {e}")
            raise FileLoaderExcpError(f"Failed to parse YAML file: {e}") from e
        return data

    def _validate_structure(self, data: dict):
        if not isinstance(data, dict) or self.key_name not in data:
            self.logger.error(f"YAML must contain '{self.key_name}' key")
            raise FileLoaderExcpError(f"YAML must contain '{self.key_name}' key")
        items = data[self.key_name]
        if not isinstance(items, list):
            self.logger.error(f"'{self.key_name}' must be a list")
            raise FileLoaderExcpError(f"'{self.key_name}' must be a list")
        return items

    def _validate_duplicates(self, items: list[dict]):
        duplicates = self._check_duplicates(items)
        if duplicates:
            self.logger.error(f"Duplicate {self.id_field}s found: {duplicates}")
            raise FileLoaderExcpError(f"Duplicate {self.id_field}s found: {duplicates}")

    def _validate_items(self, items: list[dict]) -> list[T]:
        validated_items: list[T] = []
        for i, item in enumerate(items):
            try:
                validated_items.append(self.model(**item))
            except ValidationError as e:
                self.logger.error(f"Validation failed at index {i}: {e}")
                raise FileLoaderExcpError(f"Validation failed at index {i}: {e}") from e
        return validated_items

    def __init__(self, key_name: str, id_field: str, model: type[T], logger: Any):
        """key_name: nama key utama di YAML (misal: 'members').

        id_field: nama field yang jadi unique id (misal: 'memberid')
        model: Pydantic model untuk validasi
        logger: custom logger instance
        """
        self.key_name = key_name
        self.id_field = id_field
        self.model = model
        self.logger = logger

    def _check_duplicates(self, items: list[dict]) -> list[str]:
        seen = set()
        duplicates = []
        for item in items:
            item_id = item.get(self.id_field)
            if item_id in seen:
                duplicates.append(item_id)
            else:
                seen.add(item_id)
        return duplicates

    def load_and_validate(self, yaml_path: Path) -> list[T]:
        """Load YAML, validasi struktur, duplicate, dan schema pydantic."""
        self._check_file_exists(yaml_path)
        data = self._parse_yaml(yaml_path)
        items = self._validate_structure(data)
        self._validate_duplicates(items)
        validated_items = self._validate_items(items)
        self.logger.bind(operation="yaml_loader.load_and_validate").info(
            f"Loaded {len(validated_items)} {self.key_name} from {yaml_path}"
        )
        return validated_items
