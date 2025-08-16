"""ini base untuk seeding data awal aja."""

from typing import Any

from app.custom.exc_exceptions import ServiceExcpError, UploaderExcpError
from app.mlogg import logger


class BaseUploader:
    """Base uploader dengan fail-fast, contextual logging, dan error handling."""

    uploader_name: str = "BaseUploader"  # override di subclass

    def __init__(self, service: Any):
        self._service = service
        self._log = logger.bind(uploader=self.uploader_name)

    def upload(self, data: dict[str, Any]) -> None:
        """Upload data dict ke service.

        Args:
            data (dict[str, Any]): key-value data yang akan diupload.
        """
        log = self._log.bind(operation="upload")
        try:
            for key, entity in data.items():
                self._service.add(key, entity)
            log.info(f"Total {len(data)} entity berhasil diupload")
        except ServiceExcpError:
            log.exception("Service gagal saat upload")
            raise
        except Exception as e:
            log.exception("Uploader gagal upload")
            raise UploaderExcpError(f"{self.uploader_name} gagal upload") from e
