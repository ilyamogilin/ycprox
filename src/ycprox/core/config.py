from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, model_validator
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="YCPROX_",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    debug: bool = Field(
        default=True,
        description="Debug mode"
    )

    cli_name: str = Field(
        default="ycprox",
        description="Name of the CLI",
        exclude=True
    )

    version: str = Field(
        default="0.1.1", 
        description="Version of the application",
        exclude=True
    )

    folder_id: Optional[str] = Field(
        default=None,
        description="Folder ID to deploy proxy-gateway",
    )

    ua_string: Optional[str] = Field(
        default=None, 
        description="User-Agent string for HTTP requests",
    )

    @model_validator(mode='after')
    def set_ua_string_default(self) -> 'Settings':
        if self.ua_string is None:
            self.ua_string = f"ycprox/{self.version}"
        return self


settings = Settings()

