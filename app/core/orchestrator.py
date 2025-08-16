from pathlib import Path
from typing import Any

from app.config import get_settings
from app.core.async_watcher import AsyncFileWatcher
from app.domain.member.srv_member import MemberService
from app.domain.module.srv_module import ModuleService
from app.mlogg import logger
from app.services.uploader import MemberUploader, ModuleUploader

PATHMEMBER = Path(get_settings().config_path) / "members.yaml"
PATHMODULE = Path(get_settings().config_path) / "modules.yaml"


class AppOrchestrator:
    """Orchestrator: init service, seeder, async watcher + auto reload YAML."""

    def __init__(self, logger: Any = logger):
        self.logger = logger
        self.member_service: MemberService = MemberService()
        self.module_service: ModuleService = ModuleService()
        self.watcher: AsyncFileWatcher = AsyncFileWatcher()

    async def init_services(self):
        """Clear repos & seed initial data async (fail-safe)."""
        # Step 1: Clear repos
        try:
            self.member_service._repo.clear()
            self.module_service._repo.clear()
            self.logger.info("✅ Repos cleared")
        except Exception as e:
            self.logger.exception("❌ Failed to clear repos")
            raise RuntimeError(f"Failed to clear repos: {e}") from e

        # Step 2: Seed data awal (fail-safe)
        try:
            await MemberUploader(self.member_service).upload_from_yaml(PATHMEMBER)
            await ModuleUploader(self.module_service).upload_from_yaml(PATHMODULE)
            self.logger.info("✅ Initial data seeded for Member & Module")
        except Exception as e:
            self.logger.error(f"❌ Failed to seed initial data: {e}")
            # tetap lanjut meskipun ada error

    def setup_watchers(self):
        """Register watcher untuk auto reload setiap YAML perubahan."""

        async def reload_members():
            try:
                await MemberUploader(self.member_service).upload_from_yaml(PATHMEMBER)
                self.logger.info("♻ Members reloaded via watcher")
            except Exception as e:
                self.logger.error(f"❌ Watcher failed reload members: {e}")

        async def reload_modules():
            try:
                await ModuleUploader(self.module_service).upload_from_yaml(PATHMODULE)
                self.logger.info("♻ Modules reloaded via watcher")
            except Exception as e:
                self.logger.error(f"❌ Watcher failed reload modules: {e}")

        self.watcher.add_watch(PATHMEMBER, reload_members)
        self.watcher.add_watch(PATHMODULE, reload_modules)
        self.logger.info("👀 Watchers registered for YAML configs")

    async def start_watchers(self):
        """Start semua watcher async."""
        await self.watcher.start()
        self.logger.info("🚀 Async watchers started")

    async def stop_watchers(self):
        """Stop semua watcher async."""
        await self.watcher.stop()
        self.logger.info("🛑 Async watchers stopped")

    # Getter untuk domain service
    def get_member_service(self) -> MemberService:
        return self.member_service

    def get_module_service(self) -> ModuleService:
        return self.module_service
