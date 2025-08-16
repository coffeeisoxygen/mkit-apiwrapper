from pathlib import Path

import yaml

from app.core.datalayer import BaseUploader
from app.custom.exc_exceptions import UploaderExcpError
from app.domain.member.sch_member import MemberInDB
from app.domain.member.srv_member import MemberService
from app.mlogg import logger


class MemberUploader(BaseUploader):
    uploader_name = "MemberUploader"

    def __init__(self, service: MemberService):
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
                raise ValueError("YAML format invalid untuk MemberUploader")

            members = raw.get("members", [])
            data_models = {}
            for item in members:
                key = item["memberid"]
                data_models[key] = MemberInDB(**item)

            self.upload(data_models)
            log.info(f"Total {len(data_models)} member berhasil diupload")

        except Exception as e:
            log.exception("Uploader gagal upload dari YAML")
            raise UploaderExcpError(
                f"{self.uploader_name} gagal upload_from_yaml"
            ) from e
