from ycprox.ycloud.client import get_apigateway_service, get_sdk
from yandex.cloud.serverless.apigateway.v1.apigateway_service_pb2 import (
    CreateApiGatewayRequest, 
    CreateApiGatewayMetadata, 
    DeleteApiGatewayRequest, 
    DeleteApiGatewayMetadata,
) 
from yandex.cloud.serverless.apigateway.v1.apigateway_pb2 import ApiGateway

def create_api_gateway(folder_id: str, name: str, openapi_spec: str) -> tuple[str, str]:
    """Create an API gateway."""
    service = get_apigateway_service()
    operation = service.Create(CreateApiGatewayRequest(
        folder_id=folder_id,
        name=name,
        openapi_spec=openapi_spec,
    ))

    sdk = get_sdk()
    result = sdk.wait_operation_and_get_result(
        operation=operation,
        response_type=ApiGateway,
        meta_type=CreateApiGatewayMetadata,
    )

    return (result.response.id, result.response.domain)

def delete_api_gateway(gateway_id: str) -> bool:
    """Delete an API gateway.
    
    Returns True if operation completed successfully, False otherwise.
    """
    service = get_apigateway_service()
    operation = service.Delete(DeleteApiGatewayRequest(
        api_gateway_id=gateway_id,
    ))

    sdk = get_sdk()
    
    # wait_operation_and_get_result raises exception on failure
    # For delete, response is empty (google.protobuf.Empty)
    sdk.wait_operation_and_get_result(
        operation=operation,
        meta_type=DeleteApiGatewayMetadata,
    )
    
    # If we reach here without exception, operation succeeded
    return True