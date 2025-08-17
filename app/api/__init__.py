from app.api.v1.debug.debug import router as debug_router
from app.api.v1.members import router as member_router


def register_routers(app):  # noqa: ANN001, D103
    app.include_router(
        debug_router,
        prefix="/api/v1",
        tags=["Debug"],
    )

    app.include_router(
        member_router,
        prefix="/api/v1",
        tags=["Members"],
    )
