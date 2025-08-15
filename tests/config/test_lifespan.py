import pytest
from app.config.cfg_lifespan import app_lifespan


@pytest.mark.asyncio
async def test_app_lifespan_logs(monkeypatch):
    logs = []

    class DummyLogger:
        def bind(self, **kwargs):
            return self

        def info(self, msg):
            logs.append(msg)

    def dummy_init_logging():
        logs.append("init_logging_called")

    monkeypatch.setattr("app.config.cfg_lifespan.logger", DummyLogger())
    monkeypatch.setattr("app.config.cfg_lifespan.init_logging", dummy_init_logging)

    dummy_app = object()
    async with app_lifespan(dummy_app):
        pass

    assert "init_logging_called" in logs
    assert "Starting application" in logs
    assert "Shutting down application..." in logs
