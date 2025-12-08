from typing import Optional
from pydantic import BaseModel, Field, model_validator
from ycprox.core.config import settings


class ProxySettings(BaseModel):
    """Shared proxy settings model for up/down commands."""

    name: str = Field(description="Name of the proxy gateway", default="proxy-gateway")
    folder_id: Optional[str] = Field(default=None, description="Folder ID to deploy proxy-gateway")
    
    # Not a CLI arg - populated after gateway creation
    gateway_id: Optional[str] = Field(default=None, json_schema_extra={"cli": False})

    @model_validator(mode='after')
    def set_defaults_from_env(self) -> 'ProxySettings':
        if self.folder_id is None:
            self.folder_id = settings.folder_id
        return self
