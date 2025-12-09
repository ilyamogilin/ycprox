from pydantic import BaseModel

from ycprox.cli.proxy.model import ProxySettings
from ycprox.core.secrets import vault
from ycprox.ycloud.apigateway import delete_api_gateway
from ycprox.ycloud.cloudfunction import delete_cloud_function


class ProxyAppDown(BaseModel):
    """Use this command to tear down the proxy gateway."""

    def cli_cmd(self) -> None:
        # Retrieve saved settings from vault
        saved_settings = vault.pop_proxy_settings()
        
        if saved_settings is None:
            print("No proxy settings found. Was the proxy started with 'up' command?")
            return
        
        # Reconstruct ProxySettings from saved data
        proxy = ProxySettings.model_validate(saved_settings)
        
        if not proxy.gateway_id:
            print("No gateway_id found in saved settings.")
            return

        if not proxy.function_id:
            print("No function_id found in saved settings.")
            return

        print(f"Deleting Cloud Function '{proxy.cf_name}' (ID: {proxy.function_id})...")
        
        success = delete_cloud_function(proxy.function_id)
        
        if success:
            print("Cloud Function deleted successfully!")
        else:
            print("Failed to delete Cloud Function.")
        print(f"Deleting API Gateway '{proxy.gw_name}' (ID: {proxy.gateway_id})...")
        
        success = delete_api_gateway(proxy.gateway_id)
        
        if success:
            print("API Gateway deleted successfully!")
        else:
            print("Failed to delete API Gateway.")
