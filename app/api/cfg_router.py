"""registrasi router dsini."""

from app.api.v1.debug.debug import router as debug_router


def register_routers(app):  # noqa: ANN001, D103
    app.include_router(debug_router)
