"""schemas dasar untuk members/ consumers api / otomax."""

import ipaddress

from pydantic import (
    AnyHttpUrl,
    BaseModel,
    ConfigDict,
    Field,
    SecretStr,
    field_validator,
)


class MemberInDB(BaseModel):
    """deskripsi Data Member Pada Data."""

    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
        json_schema_extra={
            "example": {
                "memberid": "M12345",
                "name": "John Doe",
                "pin": "1234",
                "password": "password",
                "is_active": True,
                "ipaddress": "192.168.1.1",
                "report_url": "http://example.com/report",
            }
        },
    )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, MemberInDB):
            return self.memberid == other.memberid
        return False

    def __hash__(self):
        return hash(self.memberid)

    memberid: str = Field(
        ..., description="ID unik untuk member", min_length=5, pattern=r"^[a-zA-Z0-9]*$"
    )
    name: str = Field(
        ..., description="Nama member", min_length=2, pattern=r"^[\w\s\-\.]{1,100}$"
    )
    pin: SecretStr = Field(..., description="PIN untuk member", min_length=6)
    password: SecretStr = Field(..., description="Password untuk member", min_length=6)

    ip_address: ipaddress.IPv4Address = Field(
        ..., alias="ipaddress", description="Alamat IP member"
    )
    report_url: AnyHttpUrl = Field(..., description="URL untuk laporan member")
    is_active: bool = Field(default=True, description="Status keaktifan member")
    report_url: AnyHttpUrl = Field(..., description="URL untuk laporan member")
    is_active: bool = Field(default=True, description="Status keaktifan member")

    allow_nosign: bool = Field(
        default=False,
        description="member akan bertransaksi tanpa otomax sign jika di set true",
    )

    @field_validator("pin", "password", mode="before")
    @classmethod
    def validate_secret_fields(cls, v: str | None) -> str:
        if v is None or not v:
            raise ValueError("Field is required")
        if isinstance(v, int):
            return str(v)
        return v
