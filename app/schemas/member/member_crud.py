"""schemas dasar untuk members/ consumers api / otomax."""

from datetime import datetime

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field, IPvAnyAddress, SecretStr


class MemberBase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
        from_attributes=True,
    )

    memberid: str = Field(
        ..., description="ID unik untuk member", min_length=5, pattern=r"^[a-zA-Z0-9]*$"
    )
    name: str = Field(
        ..., description="Nama member", min_length=2, pattern=r"^[\w\s\-\.]{1,100}$"
    )
    ipaddress: IPvAnyAddress = Field(..., description="Alamat IP member")
    report_url: AnyHttpUrl = Field(..., description="URL untuk laporan member")


class MemberCreate(MemberBase):
    """Schema untuk membuat member baru (plaintext pin/password, di-hash oleh service)."""

    pin: SecretStr = Field(..., description="PIN untuk member", min_length=6)
    password: SecretStr = Field(..., description="Password untuk member", min_length=6)

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
                "pin": "123456",
                "password": "secret123",
            }
        },
    )


class MemberRead(MemberBase):
    is_active: bool = Field(description="Status keaktifan member")
    allow_nosign: bool = Field(
        description="member akan bertransaksi tanpa otomax sign jika di set true",
    )
    created_at: datetime = Field(description="Waktu pembuatan member")
    updated_at: datetime = Field(description="Waktu pembaruan member")

    model_config = ConfigDict(from_attributes=True)


class MemberUpdate(BaseModel):
    """schema untuk update data member."""

    name: str | None = Field(
        None, description="Nama member", min_length=2, pattern=r"^[\w\s\-\.]{1,100}$"
    )
    ipaddress: IPvAnyAddress | None = Field(None, description="Alamat IP member")
    report_url: AnyHttpUrl | None = Field(None, description="URL untuk laporan member")
    is_active: bool | None = Field(None, description="Status keaktifan member")
    allow_nosign: bool | None = Field(
        None,
        description="member akan bertransaksi tanpa otomax sign jika di set true",
    )

    model_config = ConfigDict(extra="forbid", from_attributes=True)


class MemberDelete(BaseModel):
    """Schema untuk menghapus member (hard delete)."""

    memberid: str = Field(..., description="ID unik untuk member")
