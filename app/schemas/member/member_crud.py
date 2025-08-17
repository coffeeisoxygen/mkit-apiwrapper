"""schemas dasar untuk members/ consumers api / otomax."""

from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    SecretStr,
)


class MemberBase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
        from_attributes=True,
    )
    """Schema dasar untuk member."""

    memberid: str = Field(
        ..., description="ID unik untuk member", min_length=5, pattern=r"^[a-zA-Z0-9]*$"
    )
    name: str = Field(
        ..., description="Nama member", min_length=2, pattern=r"^[\w\s\-\.]{1,100}$"
    )
    ipaddress: str = Field(..., description="Alamat IP member")
    report_url: str = Field(..., description="URL untuk laporan member")


class MemberCreate(MemberBase):
    """Schema untuk membuat member baru."""

    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
        from_attributes=True,
        json_schema_extra={
            "example": {
                "memberid": "M12345",
                "name": "John Doe",
                "ipaddress": "192.168.1.1",
                "report_url": "http://example.com/report",
                "hash_pin": "hashed_pin",
                "hash_password": "hashed_password",
            }
        },
    )

    hash_pin: SecretStr = Field(..., description="PIN untuk member", min_length=6)
    hash_password: SecretStr = Field(
        ..., description="Password untuk member", min_length=6
    )


class MemberRead(MemberBase):
    is_active: bool = Field(description="Status keaktifan member")
    allow_nosign: bool = Field(
        description="member akan bertransaksi tanpa otomax sign jika di set true",
    )
    created_at: datetime = Field(description="Waktu pembuatan member")
    updated_at: datetime = Field(description="Waktu pembaruan member")


class MemberUpdate(BaseModel):
    """schema untuk update data member."""

    name: str | None = Field(
        None, description="Nama member", min_length=2, pattern=r"^[\w\s\-\.]{1,100}$"
    )
    ipaddress: str | None = Field(None, description="Alamat IP member")
    report_url: str | None = Field(None, description="URL untuk laporan member")
    is_active: bool | None = Field(None, description="Status keaktifan member")
    allow_nosign: bool | None = Field(
        None,
        description="member akan bertransaksi tanpa otomax sign jika di set true",
    )

    model_config = ConfigDict(extra="forbid")


class MemberDelete(BaseModel):
    memberid: str = Field(..., description="ID unik untuk member")
    is_active: bool = Field(..., description="Status keaktifan member")
