from fastapi import APIRouter

from app.deps import DepAppSettings

router = APIRouter()


@router.get("/settings")
def get_settings(app_settings: DepAppSettings):
    return app_settings
