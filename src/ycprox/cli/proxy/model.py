from typing import Optional
from pydantic import BaseModel, Field, model_validator
from pydantic_settings import CLI_SUPPRESS
from ycprox.core.config import settings


class ProxySettings(BaseModel):
    """Shared proxy settings model for up/down commands."""

    url: str = Field(description="URL of the destination service to proxy requests to")
    name: str = Field(default="proxy-gateway", description="Name of the proxy gateway")
    folder_id: Optional[str] = Field(default=None, description="Folder ID to deploy proxy-gateway")
    
    # Non-CLI args - populated after resources creation
    gateway_id: Optional[str] = Field(default=None, description=CLI_SUPPRESS)
    function_id: Optional[str] = Field(default=None, description=CLI_SUPPRESS)

    @model_validator(mode='after')
    def set_defaults_from_env(self) -> 'ProxySettings':
        if self.folder_id is None:
            self.folder_id = settings.folder_id
        return self
