"""register exceptions here."""

from fastapi import Request
from fastapi.responses import JSONResponse

from app.custom.exc_exceptions import AppExceptionError
from app.mlogg import logger


def init_exceptions(app):  # noqa: ANN001, D103
    @app.exception_handler(AppExceptionError)
    async def app_exception_handler(request: Request, exc: AppExceptionError):  # noqa: ARG001, RUF029
        logger.error(f"Application error: {exc.message}", extra=exc.context)
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.message, "context": exc.context},
        )
