"""CORS Configuration."""

from fastapi.middleware.cors import CORSMiddleware

# TODO: Nanti Buat Setup Origins , Rate Limiting , dan Lain Lain.


def init_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
