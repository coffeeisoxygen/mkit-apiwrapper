from abc import ABC, abstractmethod
from collections.abc import Sequence

from app.models.member import Member


class IMemberRepository(ABC):
    """Kontrak repository untuk entitas Member."""

    @abstractmethod
    async def create(self, member: Member) -> Member:
        """Simpan member baru ke database."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, member_id: str) -> Member | None:
        """Ambil member berdasarkan ID unik."""
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> Sequence[Member]:
        """Ambil semua member (perlu pagination kalau data besar)."""
        raise NotImplementedError

    @abstractmethod
    async def update(self, member: Member) -> Member:
        """Update data member yang sudah ada."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, member: Member) -> None:
        """Hapus member dari database."""
        raise NotImplementedError
