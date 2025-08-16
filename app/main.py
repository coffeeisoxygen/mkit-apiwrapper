import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.cfg_router import register_routers
from app.config import get_settings, version
from app.config.cfg_lifespan import app_lifespan
from app.custom.exc_exceptions import AppExceptionError
from app.mlogg import logger

# import settings
settings = get_settings()

app: FastAPI = FastAPI(
    title="mkit-apiwrapper",
    description="project untuk hanlde dan wrapper response dari Module Module API otoplus",
    version=version,
    lifespan=app_lifespan,
)


# Global exception handler for custom exceptions
@app.exception_handler(AppExceptionError)
async def app_exception_handler(request: Request, exc: AppExceptionError):  # noqa: ARG001, D103, RUF029
    logger.error(f"Application error: {exc.message}", extra=exc.context)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message, "context": exc.context},
    )


register_routers(app)


# just main root
@app.get("/", tags=["Root"])
async def read_root():
    """Just root."""
    return {
        "message": "Welcome to mkit-apiwrapper",
        "version": version,
        "settings": settings.model_dump(),
    }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", host="0.0.0.0", port=8000, log_level="info", reload=True
    )
