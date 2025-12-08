from yandex.cloud.serverless.apigateway.v1.apigateway_service_pb2 import (
    CreateApiGatewayRequest,
    CreateApiGatewayMetadata,
)
from yandex.cloud.serverless.apigateway.v1.apigateway_pb2 import ApiGateway

from ycprox.cli.proxy.model import ProxySettings
from ycprox.core.secrets import vault
from ycprox.core.apispec import API_SPEC
from ycprox.core.yc_client import get_sdk, get_apigateway_service


class ProxyAppUp(ProxySettings):
    """Use this command to spin up the proxy gateway.\nDo not forget to authenticate in Yandex first using the `ycprox auth` command."""

    def cli_cmd(self) -> None:
        print(f"Creating API Gateway '{self.name}' in folder '{self.folder_id}'...")
        
        service = get_apigateway_service()
        operation = service.Create(CreateApiGatewayRequest(
            folder_id=self.folder_id,
            name=self.name,
            openapi_spec=API_SPEC,
        ))
        
        # Wait for operation to complete
        sdk = get_sdk()
        result = sdk.wait_operation_and_get_result(
            operation,
            response_type=ApiGateway,
            meta_type=CreateApiGatewayMetadata,
        )
        
        # Extract gateway_id from the response
        self.gateway_id = result.response.id
        
        print(f"API Gateway created successfully!")
        print(f"Gateway ID: {self.gateway_id} on url https://{result.response.domain}/")
        
        # Save settings for later use by down command
        vault.save_proxy_settings(self.model_dump())