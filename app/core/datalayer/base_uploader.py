"""ini base untuk seeding data awal aja."""

import inspect
from typing import Any

from app.custom.exc_exceptions import ServiceExcpError, UploaderExcpError
from app.mlogg import logger


class BaseUploader:
    """Base uploader dengan fail-fast, contextual logging, dan error handling."""

    uploader_name: str = "BaseUploader"  # override di subclass

    def __init__(self, service: Any):
        self._service = service
        self._log = logger.bind(uploader=self.uploader_name)

    async def upload(self, data: dict[str, Any]) -> None:
        log = self._log.bind(operation="upload")
        try:
            for key, entity in data.items():
                add_method = getattr(self._service, "add", None)
                if add_method is not None and callable(add_method):
                    if inspect.iscoroutinefunction(add_method):
                        await add_method(key, entity)
                    else:
                        add_method(key, entity)
            log.info(f"Total {len(data)} entity berhasil diupload")
        except ServiceExcpError:
            log.exception("Service gagal saat upload")
            raise
        except Exception as e:
            log.exception("Uploader gagal upload")
            raise UploaderExcpError(f"{self.uploader_name} gagal upload") from e
