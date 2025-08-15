import asyncio
from collections.abc import Callable
from pathlib import Path
from typing import Any

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from app.mlogg import logger


def _normalize_path(path: str | Path) -> Path:
    """Helper to resolve and normalize a path for comparison."""
    return Path(path).resolve()


class AsyncChangeHandler(FileSystemEventHandler):
    """Handler yang trigger callback async dengan debounce."""

    def __init__(
        self, file_path: Path, callback: Callable[[], Any], debounce: float = 1.0
    ):
        super().__init__()
        self.file_path = file_path.resolve()
        self.callback = callback
        self.debounce = debounce
        self._task: asyncio.Task | None = None

    def on_modified(self, event: FileSystemEvent):
        src_path = event.src_path
        if isinstance(src_path, bytes):
            src_path = src_path.decode()
        event_path = _normalize_path(src_path)
        if event_path == self.file_path and not event.is_directory:
            logger.info(
                f"📄 {self.file_path.name} changed, debouncing {self.debounce}s"
            )
            if self._task and not self._task.done():
                self._task.cancel()
            self._task = asyncio.create_task(self._debounced_callback())

    async def _debounced_callback(self):
        try:
            await asyncio.sleep(self.debounce)
            if asyncio.iscoroutinefunction(self.callback):
                await self.callback()
            else:
                self.callback()
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"❌ Error in watcher callback: {e}")


class AsyncFileWatcher:
    """Async watcher untuk multiple YAML file."""

    def __init__(self):
        self._observer = Observer()
        self._handlers: list[AsyncChangeHandler] = []

    def add_watch(
        self, file_path: Path, callback: Callable[[], Any], debounce: float = 1.0
    ):
        handler = AsyncChangeHandler(file_path, callback, debounce)
        self._observer.schedule(handler, str(file_path.parent), recursive=False)
        self._handlers.append(handler)
        logger.info(f"👀 Watching {file_path.name} async")

    async def start(self):
        """Start observer non-blocking."""
        self._observer.start()
        logger.info("🚀 Async file watcher started")

    async def stop(self):
        """Stop observer cleanly."""
        for h in self._handlers:
            if h._task and not h._task.done():
                h._task.cancel()
        self._observer.stop()
        self._observer.join()
        logger.info("🛑 Async file watcher stopped")
