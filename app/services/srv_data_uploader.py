from pathlib import Path
from typing import Any  # <-- Add this import

import aiofiles
import yaml

from app.mlogg import logger


class DataUploader:
    def __init__(self, repo: Any, schema: Any, key_field: str, data_field: str):
        """Generic uploader untuk data.

        repo: repository instance
        schema: pydantic/model class
        key_field: nama field unik (misal 'memberid', 'moduleid')
        data_field: nama field utama di yaml (misal 'members', 'modules')
        """
        self.repo = repo
        self.schema = schema
        self.key_field = key_field
        self.data_field = data_field
        self._log = logger.bind(uploader="DataUploader")

    async def upload_from_yaml(self, path: str | Path):
        log = self._log.bind(operation="upload_from_yaml", path=str(path))
        try:
            p = Path(path)
            async with aiofiles.open(p, encoding="utf-8") as f:
                content = await f.read()
            raw = yaml.safe_load(content)

            if not isinstance(raw, dict):
                log.error("YAML format invalid, harus dict")
                return

            items = raw.get(self.data_field, [])
            for item in items:
                key = item[self.key_field]
                model = self.schema(**item)
                self.repo.upsert(key, model)
            log.info(f"Total {len(items)} {self.data_field} berhasil diupload")
        except Exception:
            log.exception("Uploader gagal upload dari YAML")
