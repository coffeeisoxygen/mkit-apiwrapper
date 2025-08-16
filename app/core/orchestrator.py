from pathlib import Path
from typing import Any

from app.config import get_settings
from app.core.async_watcher import AsyncFileWatcher
from app.domain.member.rep_member import MemberRepository
from app.domain.member.sch_member import MemberInDB
from app.domain.module.rep_module import ModuleRepository
from app.domain.module.sch_module import ModuleInDB
from app.mlogg import logger
from app.services.srv_data_uploader import DataUploader

PATHMEMBER = Path(get_settings().config_path) / "members.yaml"
PATHMODULE = Path(get_settings().config_path) / "modules.yaml"


class AppOrchestrator:
    """Orchestrator: init service, seeder, async watcher + auto reload YAML."""

    def __init__(self, logger: Any = logger):
        self.logger = logger
        self.member_repo = MemberRepository()
        self.module_repo = ModuleRepository()
        self.member_uploader = DataUploader(
            repo=self.member_repo,
            schema=MemberInDB,
            key_field="memberid",
            data_field="members",
        )
        self.module_uploader = DataUploader(
            repo=self.module_repo,
            schema=ModuleInDB,
            key_field="moduleid",
            data_field="modules",
        )
        self.watcher: AsyncFileWatcher = AsyncFileWatcher()

    async def init_services(self):
        """Clear repos & seed initial data async (fail-safe)."""
        # Step 1: Clear repos
        try:
            self.member_repo.clear()
            self.module_repo.clear()
            self.logger.info("✅ Repos cleared")
        except Exception as e:
            self.logger.exception("❌ Failed to clear repos")
            raise RuntimeError(f"Failed to clear repos: {e}") from e

        # Step 2: Seed data awal (fail-safe)
        try:
            await self.member_uploader.upload_from_yaml(PATHMEMBER)
            await self.module_uploader.upload_from_yaml(PATHMODULE)
            self.logger.info("✅ Initial data seeded for Member & Module")
        except Exception as e:
            self.logger.error(f"❌ Failed to seed initial data: {e}")
            # tetap lanjut meskipun ada error

    def setup_watchers(self):
        """Register watcher untuk auto reload setiap YAML perubahan."""

        async def reload_members():
            try:
                await self.member_uploader.upload_from_yaml(PATHMEMBER)
                self.logger.info("♻ Members reloaded via watcher")
            except Exception as e:
                self.logger.error(f"❌ Watcher failed reload members: {e}")

        async def reload_modules():
            try:
                await self.module_uploader.upload_from_yaml(PATHMODULE)
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
    def get_member_repo(self) -> MemberRepository:
        return self.member_repo

    def get_module_repo(self) -> ModuleRepository:
        return self.module_repo
