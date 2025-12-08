from pydantic import BaseModel
from yandex.cloud.serverless.apigateway.v1.apigateway_service_pb2 import DeleteApiGatewayRequest

from ycprox.cli.proxy.model import ProxySettings
from ycprox.core.secrets import vault
from ycprox.ycloud.client import get_sdk, get_apigateway_service


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
        
        print(f"Deleting API Gateway '{proxy.gw_name}' (ID: {proxy.gateway_id})...")
        
        service = get_apigateway_service()
        operation = service.Delete(DeleteApiGatewayRequest(
            api_gateway_id=proxy.gateway_id,
        ))
        
        # Wait for operation to complete
        sdk = get_sdk()
        sdk.wait_operation_and_get_result(operation)
        
        print("API Gateway deleted successfully!")
