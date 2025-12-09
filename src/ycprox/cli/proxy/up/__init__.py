from ycprox.cli.proxy.model import ProxySettings
from ycprox.core.secrets import vault
from ycprox.helpers.apispec import API_SPEC
from ycprox.ycloud.apigateway import create_api_gateway
from ycprox.ycloud.cloudfunction import deploy_cloud_function, make_public_function
from ycprox.core.config import settings

class ProxyAppUp(ProxySettings):
    """Use this command to spin up the proxy gateway.\nDo not forget to authenticate in Yandex first using the `ycprox auth` command."""

    def cli_cmd(self) -> None:

        function_id, version_id = deploy_cloud_function(
            folder_id=self.folder_id,
            name=self.cf_name,
            destination_url=self.url
        )

        print(f"Cloud Function created successfully!")
        print(f"Function ID: {function_id} on version {version_id}")

        success = make_public_function(function_id)
        
        if not success:
            print(f"Failed to make Cloud Function publicly accessible.")
            return

        print(f"Creating API Gateway '{self.gw_name}' in folder '{self.folder_id}'...")
        
        gateway_id, domain = create_api_gateway(
            folder_id=self.folder_id, 
            name=self.gw_name, 
            openapi_spec=API_SPEC.format(function_id=function_id, version=settings.version)
        )
        
        print(f"API Gateway created successfully!")
        print(f"Gateway ID: {gateway_id} on url https://{domain}/")
        
        # Save settings for later use by down command
        self.gateway_id = gateway_id
        self.function_id = function_id

        vault.save_proxy_settings(self.model_dump())