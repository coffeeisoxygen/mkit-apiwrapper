"""schemas untuk account2 API."""

from pydantic import AnyHttpUrl, BaseModel, EmailStr, Field, SecretStr, field_validator

from app.config import ProviderEnums


class ModuleInDB(BaseModel):
    """schema untuk module module API."""

    model_config = {
        "populate_by_name": True,
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "moduleid": "module123",
                "provider": "DIGIPOS",
                "name": "Module Name",
                "username": "user123",
                "msisdn": "08123456789",
                "pin": "1234",
                "password": "securepassword",
                "email": "user123@example.com",
                "is_active": True,
                "base_url": "https://api.example.com/modules/module123",
            }
        },
    }

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ModuleInDB):
            return self.moduleid == other.moduleid
        return False

    def __hash__(self):
        return hash(self.moduleid)

    moduleid: str = Field(
        pattern=r"^[a-zA-Z0-9_]+$",
        min_length=3,
        max_length=10,
        description="ID unik untuk module, ini di gunakan untuk authtentikasi dan yang akan di HIT oleh API as &moduleid=moduleid",
    )
    provider: ProviderEnums = Field(
        description="Provider untuk module",
    )
    name: str = Field(
        min_length=3,
        max_length=100,
        description="Nama untuk module",
    )
    username: SecretStr = Field(
        min_length=3,
        max_length=100,
        description="Username untuk module",
    )
    msisdn: SecretStr = Field(
        min_length=3,
        max_length=100,
        description="MSISDN untuk module",
    )
    pin: SecretStr = Field(
        min_length=3,
        max_length=100,
        description="PIN untuk module",
    )
    password: SecretStr = Field(
        min_length=8,
        max_length=100,
        description="Password untuk module",
    )
    email: EmailStr = Field(
        min_length=3,
        max_length=100,
        description="Email untuk module",
    )
    is_active: bool = Field(
        description="Status aktif untuk module",
    )
    base_url: AnyHttpUrl = Field(
        description="Base URL untuk module",
    )

    @field_validator("username", "msisdn", "pin", "password", mode="before")
    @classmethod
    def validate_secret_fields(cls, v: str | None) -> str:
        if v is None or not v:
            raise ValueError("Field is required")
        if isinstance(v, int):
            return str(v)
        return v
