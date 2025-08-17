# intf_member.py
from abc import ABC, abstractmethod

from app.models.member import Member


class IMemberRepository(ABC):
    @abstractmethod
    async def create(self, member_data: dict) -> Member:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, member_id: str) -> Member | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[Member]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, member_id: str, member_data: dict) -> Member | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, member_id: str) -> bool:
        raise NotImplementedError
