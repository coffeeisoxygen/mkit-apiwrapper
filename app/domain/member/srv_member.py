from pathlib import Path
from typing import Any

from app.domain.member.sch_member import MemberInDB
from app.utils.loader.yaml_loader import YAMLDataImporter

KEYNAME = "members"
IDFIELD = "memberid"


class MemberService:
    def __init__(self, yaml_path: Path, logger: Any):
        self.yaml_path = yaml_path
        self.logger = logger
        self._members: list[MemberInDB] = []
        self._is_ready: bool = False  # internal state flag

        # Loader setup (key_name di YAML harus "members")
        self.loader = YAMLDataImporter(
            key_name=KEYNAME, id_field=IDFIELD, model=MemberInDB, logger=logger
        )

    def load_members(self) -> None:
        """Load & validate members dari YAML, update state readiness."""
        with self.logger.contextualize(
            member_count=len(self._members), path=str(self.yaml_path)
        ):
            try:
                data = self.loader.load_and_validate(self.yaml_path)

                if len(data) > 0:  # ✅ minimal ada 1 data valid
                    self._members = data
                    self._is_ready = True
                    self.logger.info(
                        f"✅ Loaded {len(self._members)} members from {self.yaml_path}"
                    )
                else:  # ⚠️ file valid tapi kosong
                    self._is_ready = False
                    self.logger.warning("⚠️ Members file loaded but no data found")

            except Exception as e:
                self._is_ready = False
                self.logger.error(f"❌ Failed to load members: {e}")
                self.logger.info("Using previous member data in memory.")

    def get_all(self) -> list[MemberInDB]:
        return self._members

    def get_by_id(self, member_id: str) -> MemberInDB | None:
        return next((m for m in self._members if m.memberid == member_id), None)

    def is_active(self, member_id: str) -> bool:
        member = self.get_by_id(member_id)
        return bool(member and member.is_active)

    @property
    def is_ready(self) -> bool:
        """True kalau:.

        - Pernah sukses load terakhir kali, DAN
        - Ada minimal 1 data valid di memory
        """
        return self._is_ready and len(self._members) > 0

    def get_status(self) -> dict[str, Any]:
        """Expose status detail untuk debug / monitoring."""
        return {
            "ready": self.is_ready,
            "count": len(self._members),
            "path": str(self.yaml_path),
        }
