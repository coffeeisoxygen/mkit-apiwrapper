from app.config import get_settings


class AppExceptionError(Exception):
    """Base exception with adapter support."""

    default_message: str = "An application error occurred."
    status_code: int = 500

    def __init__(
        self,
        message: str | None = None,
        name: str = get_settings().app_name,
        context: dict | None = None,
        cause: Exception | None = None,
    ):
        self.message = message or self.default_message
        self.name = name
        self.context = context or {}
        self.__cause__ = cause
        super().__init__(self.message)


class FileLoaderExcpError(AppExceptionError):
    """Exception raised for file-related errors."""

    default_message: str = "Ada Error Di Proses Loader Data"
    status_code: int = 400


class InternalServiceError(AppExceptionError):
    """Exception raised for internal service errors."""

    default_message: str = "Ada Error Di Proses Internal Service"
    status_code: int = 500


class InternalError(AppExceptionError):
    """Exception raised for internal errors."""

    default_message: str = "Ada Error Di Proses Internal"
    status_code: int = 500


class ValidationError(AppExceptionError):
    """Exception raised for validation errors."""

    default_message: str = "Ada Error Di Proses Validasi"
    status_code: int = 422


class ConfigExcpError(AppExceptionError):
    """Exception raised for configuration-related errors."""

    default_message: str = "Ada Error Di Proses Config"
    status_code = 500
