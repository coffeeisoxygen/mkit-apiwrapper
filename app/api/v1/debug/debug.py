"""admin router for debuging data."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "healthy"}


@router.get("/data/{item_id}")
def read_data(item_id: int):
    return {"item_id": item_id}
