from pathlib import Path
from typing import Any

from app.custom.exc_exceptions import InternalServiceError
from app.domain.member.sch_member import MemberInDB
from app.utils.loader.yaml_loader import YAMLDataImporter


class MemberService:
    def __init__(self, yaml_path: Path, logger: Any):
        self.yaml_path = yaml_path
        self.logger = logger
        self._members: list[MemberInDB] = []

        # Loader setup (key_name di YAML harus "members")
        self.loader = YAMLDataImporter(
            key_name="members", id_field="memberid", model=MemberInDB, logger=logger
        )

    def load_members(self) -> None:
        """Load dan validasi data member dari YAML ke memory."""
        try:
            self._members = self.loader.load_and_validate(self.yaml_path)
            self.logger.info(
                f"✅ Loaded {len(self._members)} members from {self.yaml_path}"
            )
        except Exception as e:
            self.logger.error(f"❌ Failed to load members: {e}")
            raise InternalServiceError(f"Failed to load members: {e}") from e

    def get_all(self) -> list[MemberInDB]:
        return self._members

    def get_by_id(self, member_id: str) -> MemberInDB | None:
        return next((m for m in self._members if m.memberid == member_id), None)

    def is_active(self, member_id: str) -> bool:
        member = self.get_by_id(member_id)
        return bool(member and member.is_active)
