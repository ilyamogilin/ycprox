from yandexcloud import SDK
from yandex.cloud.serverless.apigateway.v1.apigateway_service_pb2_grpc import ApiGatewayServiceStub
from yandex.cloud.serverless.functions.v1.function_service_pb2_grpc import FunctionServiceStub

from ycprox.core.config import settings
from ycprox.core.secrets import vault


def get_sdk() -> SDK:
    """Initialize Yandex Cloud SDK with OAuth token from vault."""
    token = vault.load_oauth_token()
    if not token:
        raise RuntimeError("Not authenticated. Run 'ycprox auth init' first.")
    return SDK(token=token, user_agent=settings.ua_string)


def get_apigateway_service() -> ApiGatewayServiceStub:
    """Get API Gateway service client."""
    return get_sdk().client(ApiGatewayServiceStub)

def get_function_service() -> FunctionServiceStub:
    """Get Function service client."""
    return get_sdk().client(FunctionServiceStub)