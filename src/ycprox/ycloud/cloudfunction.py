from google.protobuf.duration_pb2 import Duration

from ycprox.ycloud.client import get_function_service, get_sdk
from ycprox.helpers.archive_utils import create_function_zip
from yandex.cloud.serverless.functions.v1.function_service_pb2 import (
    CreateFunctionRequest,
    CreateFunctionMetadata,
    CreateFunctionVersionRequest,
    CreateFunctionVersionMetadata,
    DeleteFunctionRequest,
    DeleteFunctionMetadata,
)
from yandex.cloud.serverless.functions.v1.function_pb2 import (
    Function,
    Version,
    Resources,
)
from yandex.cloud.access.access_pb2 import (
    AccessBinding, 
    Subject, 
    SetAccessBindingsRequest, 
    SetAccessBindingsMetadata
) 


def create_cloud_function(folder_id: str, name: str) -> str:
    """Create a cloud function container (without code).
    
    Returns the function_id.
    """
    service = get_function_service()
    operation = service.Create(CreateFunctionRequest(
        folder_id=folder_id,
        name=name,
    ))

    sdk = get_sdk()
    result = sdk.wait_operation_and_get_result(
        operation,
        response_type=Function,
        meta_type=CreateFunctionMetadata,
    )

    return result.response.id


def create_function_version(
    function_id: str,
    destination_url: str,
    runtime: str = "python311",
    entrypoint: str = "index.handler",
    memory_mb: int = 128,
    timeout_seconds: int = 30,
) -> str:
    """Upload code and create a new function version.
    
    Returns the version_id.
    """
    service = get_function_service()
    
    # Create ZIP with function code
    zip_content = create_function_zip()
    
    operation = service.CreateVersion(CreateFunctionVersionRequest(
        function_id=function_id,
        runtime=runtime,
        entrypoint=entrypoint,
        resources=Resources(memory=memory_mb * 1024 * 1024),
        execution_timeout=Duration(seconds=timeout_seconds),
        content=zip_content,
        environment={"DESTINATION_BASE_URL": destination_url},
    ))

    sdk = get_sdk()
    result = sdk.wait_operation_and_get_result(
        operation,
        response_type=Version,
        meta_type=CreateFunctionVersionMetadata,
    )

    return result.response.id


def deploy_cloud_function(
    folder_id: str,
    name: str,
    destination_url: str,
    runtime: str = "python311",
    memory_mb: int = 128,
    timeout_seconds: int = 30,
) -> tuple[str, str]:
    """Create a cloud function and deploy the proxy code.
    
    Returns (function_id, version_id).
    """
    # Step 1: Create the function container
    function_id = create_cloud_function(folder_id, name)
    
    # Step 2: Upload code and create version
    version_id = create_function_version(
        function_id=function_id,
        destination_url=destination_url,
        runtime=runtime,
        memory_mb=memory_mb,
        timeout_seconds=timeout_seconds,
    )
    
    return (function_id, version_id)


def delete_cloud_function(function_id: str) -> bool:
    """Delete a cloud function.
    
    Returns True if operation completed successfully.
    """
    service = get_function_service()
    operation = service.Delete(DeleteFunctionRequest(
        function_id=function_id,
    ))

    sdk = get_sdk()
    sdk.wait_operation_and_get_result(
        operation,
        meta_type=DeleteFunctionMetadata,
    )
    
    return True


def make_public_function(function_id: str) -> bool:
    """Make a cloud function publicly accessible from the internet.
    
    Assigns the 'functions.functionInvoker' role to 'allUsers'.
    Returns True if operation completed successfully.
    """
    service = get_function_service()
    
    access_binding = AccessBinding(
        role_id="functions.functionInvoker",
        subject=Subject(
            id="allUsers",
            type="system",
        ),
    )
    
    operation = service.SetAccessBindings(SetAccessBindingsRequest(
        resource_id=function_id,
        access_bindings=[access_binding],
    ))

    sdk = get_sdk()
    sdk.wait_operation_and_get_result(
        operation,
        meta_type=SetAccessBindingsMetadata,
    )
    
    return True