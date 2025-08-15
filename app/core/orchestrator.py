from pathlib import Path
from typing import Any

from app.core.async_watcher import AsyncFileWatcher
from app.domain.member.srv_member import MemberService
from app.mlogg import logger


class AppOrchestrator:
    """Orchestrator untuk inisialisasi semua domain service dan start watcher."""

    def __init__(self, logger: Any = logger):
        self.logger = logger
        self.member_service: MemberService | None = None
        # self.product_service: ProductService | None = None
        # self.module_service: ModuleService | None = None

    def init_services(self):
        """Inisialisasi semua service dan load data awal."""
        try:
            members_yaml = Path("data/members.yaml")
            self.member_service = MemberService(members_yaml, self.logger)
            self.member_service.load_members()
            self.logger.info("✅ MemberService initialized")

            # nanti bisa di-uncomment kalau siap
            # products_yaml = Path("data/products.yaml")
            # self.product_service = ProductService(products_yaml, self.logger)
            # self.product_service.load_products()
            # self.logger.info("✅ ProductService initialized")

        except Exception as e:
            self.logger.error(f"❌ Failed to initialize services: {e}")
            raise RuntimeError(f"Failed to initialize services: {e}") from e

    def get_member_service(self) -> MemberService:
        if not self.member_service:
            raise RuntimeError("MemberService belum diinisialisasi")
        return self.member_service

    async def start(self, watcher: AsyncFileWatcher):
        """Start orchestrator tasks (watchers async)."""
        self.logger.info("🚀 Application orchestrator started")
        await watcher.start()
