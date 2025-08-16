"""schemas untuk account2 API."""

from pydantic import BaseModel, Field, SecretStr

from app.config import ProviderEnums


class ModuleInDB(BaseModel):
    moduleid: str = Field(
        pattern=r"^[a-zA-Z0-9_]+$",
        min_length=3,
        max_length=50,
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
    username: str = Field(
        min_length=3,
        max_length=100,
        description="Username untuk module",
    )
    msisdn: str = Field(
        min_length=3,
        max_length=100,
        description="MSISDN untuk module",
    )
    pin: str = Field(
        min_length=3,
        max_length=100,
        description="PIN untuk module",
    )
    password: SecretStr = Field(
        min_length=8,
        max_length=100,
        description="Password untuk module",
    )
    email: str = Field(
        min_length=3,
        max_length=100,
        description="Email untuk module",
    )
    is_active: bool = Field(
        description="Status aktif untuk module",
    )
    base_url: str = Field(
        description="Base URL untuk module",
    )
