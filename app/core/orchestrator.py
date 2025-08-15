from pathlib import Path
from typing import Any

from app.config import get_settings
from app.core.async_watcher import AsyncFileWatcher
from app.domain.member.srv_member import MemberService
from app.mlogg import logger

PATH_TOMEMBER = Path(get_settings().config_path) / "members.yaml"


class AppOrchestrator:
    """Orchestrator untuk inisialisasi semua domain service dan watcher."""

    def __init__(self, logger: Any = logger):
        self.logger = logger
        self.member_service: MemberService | None = None
        self.watcher: AsyncFileWatcher | None = None

    def init_services(self):
        """Inisialisasi semua service dan load data awal."""
        try:
            members_yaml = PATH_TOMEMBER
            self.member_service = MemberService(members_yaml, self.logger)
            self.member_service.load_members()
            self.logger.info("✅ MemberService initialized")
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize services: {e}")
            raise RuntimeError(f"Failed to initialize services: {e}") from e

    def setup_watchers(self):
        """Setup semua watcher yang dibutuhkan."""
        self.watcher = AsyncFileWatcher()
        if not self.member_service:
            raise RuntimeError(
                "MemberService belum diinisialisasi sebelum setup watcher"
            )
        self.watcher.add_watch(PATH_TOMEMBER, self.member_service.load_members)
        self.logger.info("👀 Member watcher setup")

    def get_member_service(self) -> MemberService:
        if not self.member_service:
            raise RuntimeError("MemberService belum diinisialisasi")
        return self.member_service

    async def start(self):
        """Start semua watcher async."""
        if self.watcher:
            await self.watcher.start()
            self.logger.info("🚀 All watchers started")

    async def stop(self):
        """Stop semua watcher async."""
        if self.watcher:
            await self.watcher.stop()
            self.logger.info("🛑 All watchers stopped")
