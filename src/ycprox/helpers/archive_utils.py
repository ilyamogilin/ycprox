import io
import zipfile
from pathlib import Path


# Path to the proxy serverless function code
PROXY_FUNCTION_PATH = Path(__file__).parent / "proxy_serverless.py"


def create_function_zip() -> bytes:
    """Create a ZIP archive with the proxy serverless function code."""
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        # Read and add the function code
        function_code = PROXY_FUNCTION_PATH.read_text()
        zf.writestr("index.py", function_code)
    
    return zip_buffer.getvalue()
