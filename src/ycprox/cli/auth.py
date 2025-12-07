from typing import Optional
from pydantic_settings import CliSubCommand, CliApp
from pydantic import BaseModel, Field
from ycprox.core.secrets import vault
from getpass import getpass
from ycprox.core.config import settings

oauth_url = "https://oauth.yandex.ru/authorize?response_type=token&client_id=1a6990aa636648e9b2ef855fa7bec2fb&_ym_uid=1737881378596538906&mc=v"

class Auth(BaseModel):
    """Use this command to get Yandex OAuth token to spin up the proxy"""

    def cli_cmd(self) -> None:
        print(f"Go to {oauth_url}, paste the token and press Enter to continue:")
        token = getpass("Token: ")
        vault.save_oauth_token(token)
        print("Token saved successfully")

class Proxy(BaseModel):
    name: str = Field(description="Name of the proxy", default="proxy")
    org_id: Optional[str] = Field(default=None, description="Organization ID")
    cloud_id: Optional[str] = Field(default=None, description="Cloud ID")
    folder_id: Optional[str] = Field(default=None, description="Folder ID")

    def cli_cmd(self) -> None:
        print("Proxy command")

class Application(BaseModel, cli_prog_name=settings.cli_name):
    auth: CliSubCommand[Auth]
    proxy: CliSubCommand[Proxy]

    def cli_cmd(self) -> None:
        CliApp.run_subcommand(self)