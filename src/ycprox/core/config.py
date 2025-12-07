from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="YCPROX_",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    debug: bool = True
    version: str = "0.1.0"

    ua_string: str = Field(
        default=f"ycprox/{version}", 
        description="User-Agent string for HTTP requests",
    )


settings = Settings()

