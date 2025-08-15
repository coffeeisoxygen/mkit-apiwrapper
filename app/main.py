import uvicorn
from fastapi import FastAPI

from app.config import get_settings, version

# import settings
settings = get_settings()

app: FastAPI = FastAPI(
    title="mkit-apiwrapper",
    description="project untuk hanlde dan wrapper response dari Module Module API otoplus",
    version=version,
)


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
