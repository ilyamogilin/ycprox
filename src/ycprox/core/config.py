from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, model_validator

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="YCPROX_",
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
        default="0.1.0", 
        description="Version of the application",
        exclude=True
    )

    ua_string: str | None = Field(
        default=None, 
        description="User-Agent string for HTTP requests",
    )

    @model_validator(mode='after')
    def set_ua_string_default(self) -> 'Settings':
        if self.ua_string is None:
            self.ua_string = f"ycprox/{self.version}"
        return self


settings = Settings()

