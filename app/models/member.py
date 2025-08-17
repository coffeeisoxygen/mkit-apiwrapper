"""Model Untuk Member / Concumer API / Otomax dan lain lain."""

import datetime

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base


class Member(Base):
    __tablename__ = "members"

    memberid: Mapped[str] = mapped_column(String(), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String())
    ipaddress: Mapped[str] = mapped_column(String())
    report_url: Mapped[str] = mapped_column(String())
    hash_pin: Mapped[str] = mapped_column(String())
    hash_password: Mapped[str] = mapped_column(String())
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    allow_nosign: Mapped[bool] = mapped_column(Boolean(), default=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        default=lambda: datetime.datetime.now(datetime.UTC)
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        default=lambda: datetime.datetime.now(datetime.UTC),
        onupdate=lambda: datetime.datetime.now(datetime.UTC),
    )

    def __repr__(self) -> str:
        return f"<Member memberid={self.memberid} name={self.name}>"

    def __str__(self) -> str:
        return f"Member {self.name} (ID: {self.memberid})"
