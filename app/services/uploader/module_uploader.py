from pathlib import Path

import yaml

from app.core.datalayer import BaseUploader
from app.custom.exc_exceptions import UploaderExcpError
from app.domain.module.sch_module import ModuleInDB
from app.domain.module.srv_module import ModuleService
from app.mlogg import logger


class ModuleUploader(BaseUploader):
    uploader_name = "ModuleUploader"

    def __init__(self, service: ModuleService):
        super().__init__(service)

    def upload_from_yaml(self, path: str | Path):
        log = logger.bind(
            uploader=self.uploader_name, operation="upload_from_yaml", path=str(path)
        )
        try:
            p = Path(path)
            raw = yaml.safe_load(p.read_text(encoding="utf-8"))

            if not isinstance(raw, dict):
                log.error("YAML format invalid, harus dict")
                raise ValueError("YAML format invalid untuk ModuleUploader")

            modules = raw.get("modules", [])
            data_models = {}
            for item in modules:
                key = item["moduleid"]
                data_models[key] = ModuleInDB(**item)

            self.upload(data_models)
            log.info(f"Total {len(data_models)} module berhasil diupload")

        except Exception as e:
            log.exception("Uploader gagal upload dari YAML")
            raise UploaderExcpError(
                f"{self.uploader_name} gagal upload_from_yaml"
            ) from e
