from typing import Optional
from pydantic import BaseModel, Field, model_validator
from ycprox.core.config import settings

class Proxy(BaseModel):
    """Use this command to deploy the proxy gateway.\nDo not forget to authenticate in Yandex first using the `ycprox auth` command."""

    name: str = Field(description="Name of the proxy gateway", default="proxy-gateway")
    org_id: Optional[str] = Field(default=None, description="Organization ID to deploy proxy-gateway")
    cloud_id: Optional[str] = Field(default=None, description="Cloud ID to deploy proxy-gateway")
    folder_id: Optional[str] = Field(default=None, description="Folder ID to deploy proxy-gateway")

    @model_validator(mode='after')
    def set_defaults_from_env(self) -> 'Proxy':
        if self.org_id is None:
            self.org_id = settings.org_id
        if self.cloud_id is None:
            self.cloud_id = settings.cloud_id
        if self.folder_id is None:
            self.folder_id = settings.folder_id
        return self

    def cli_cmd(self) -> None:
        print("Proxy command")
        print(f"Model dump: {self.model_dump_json()}")