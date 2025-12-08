from ycprox.cli.proxy.model import ProxySettings
from ycprox.core.secrets import vault
from ycprox.helpers.apispec import API_SPEC
from ycprox.ycloud.apigateway import create_api_gateway
from ycprox.core.config import settings

class ProxyAppUp(ProxySettings):
    """Use this command to spin up the proxy gateway.\nDo not forget to authenticate in Yandex first using the `ycprox auth` command."""

    def cli_cmd(self) -> None:
        print(f"Creating API Gateway '{self.gw_name}' in folder '{self.folder_id}'...")
        
        gateway_id, domain = create_api_gateway(
            folder_id=self.folder_id, 
            name=self.gw_name, 
            openapi_spec=API_SPEC.format(function_id="d4eo19j12tiqo3oe1jca", version=settings.version)
        )
        
        print(f"API Gateway created successfully!")
        print(f"Gateway ID: {gateway_id} on url https://{domain}/")
        
        # Save settings for later use by down command
        self.gateway_id = gateway_id
        vault.save_proxy_settings(self.model_dump())