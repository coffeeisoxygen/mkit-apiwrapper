import uvicorn
from fastapi import FastAPI

from app.config import version
from app.config.cfg_cors import init_cors
from app.config.cfg_exception import init_exceptions
from app.config.cfg_lifespan import app_lifespan
from app.config.cfg_router import register_routers

app: FastAPI = FastAPI(
    title="mkit-apiwrapper",
    description="project untuk hanlde dan wrapper response dari Module Module API otoplus",
    version=version,
    lifespan=app_lifespan,
)
init_cors(app)
register_routers(app)
init_exceptions(app)

# # Global exception handler for custom exceptions
# @app.exception_handler(AppExceptionError)
# async def app_exception_handler(request: Request, exc: AppExceptionError):
#     logger.error(f"Application error: {exc.message}", extra=exc.context)
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"error": exc.message, "context": exc.context},
#     )


# just main root
@app.get("/", tags=["Root"])
async def read_root():
    """Just root."""
    return {
        "message": "Welcome to mkit-apiwrapper",
        "version": version,
    }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", host="0.0.0.0", port=8000, log_level="info", reload=True
    )
