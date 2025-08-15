from typing import TYPE_CHECKING

from app._version import version

if TYPE_CHECKING:
    from app._version import __version__ as version
import uvicorn
from fastapi import FastAPI

app: FastAPI = FastAPI(
    title="mkit-apiwrapper",
    description="project untuk hanlde dan wrapper response dari Module Module API otoplus",
    version=version,
)


# just main root
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to mkit-apiwrapper"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", host="0.0.0.0", port=8000, log_level="info", reload=True
    )
