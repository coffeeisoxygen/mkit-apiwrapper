"""registrasi router dsini."""

from app.api.v1.debug.debug import router as debug_router


def register_routers(app):
    app.include_router(debug_router)
