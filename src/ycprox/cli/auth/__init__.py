from pydantic import BaseModel
from ycprox.core.secrets import vault
from getpass import getpass

oauth_url = "https://oauth.yandex.ru/authorize?response_type=token&client_id=1a6990aa636648e9b2ef855fa7bec2fb&_ym_uid=1737881378596538906&mc=v"

class Auth(BaseModel):
    """Use this command to get Yandex OAuth token to spin up the proxy"""

    def cli_cmd(self) -> None:
        print(f"Go to {oauth_url}, paste the token and press Enter to continue:")
        token = getpass("Token: ")
        vault.save_oauth_token(token)
        print("Token saved successfully")