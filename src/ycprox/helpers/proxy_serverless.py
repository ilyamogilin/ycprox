import base64
import os, json
from urllib.parse import urljoin, urlparse

import requests


DESTINATION_BASE_URL = os.environ.get("DESTINATION_BASE_URL", "https://webhook.site")

# Headers that should NOT be forwarded to backend
BLOCKED_REQUEST_HEADERS = {
    "uber-trace-id",
    "x-real-remote-address",
    "host",
    "x-serverless-gateway-id",
    "x-serverless-certificate-ids",
    "tracestate",
    "traceparent",
    "x-api-gateway-function-id",
    "x-envoy-external-address",
    "x-envoy-original-path",
    "x-request-id",
    "x-trace-id",
}


def build_backend_url(path: str) -> str:
    base = DESTINATION_BASE_URL.rstrip("/") + "/"
    path = (path or "/").lstrip("/")
    return urljoin(base, path)


def handler(event, context):
    print("RAW EVENT:", json.dumps(event, ensure_ascii=False))

    method = (event.get("method") or "GET").upper()
    
    proxy_value = event.get("pathParams", {}).get("proxy")
    path = "/" + proxy_value if proxy_value else "/"

    query = event.get("query") or {}
    incoming_headers = event.get("headers") or {}
    body = event.get("body")
    is_base64 = event.get("isBase64Encoded", False)

    # Decode request body
    if body is None:
        body_bytes = b""
    else:
        if is_base64:
            body_bytes = base64.b64decode(body)
        else:
            body_bytes = body.encode("utf-8")

    # Filter request headers
    outgoing_headers = {}
    for name, value in incoming_headers.items():
        if name is None or value is None:
            continue
        if name.lower() in BLOCKED_REQUEST_HEADERS:
            continue
        outgoing_headers[name] = value

    # Support X-My-X-Forwarded-For header (if provided)
    x_my = incoming_headers.get("X-My-X-Forwarded-For")

    if x_my:
        outgoing_headers["X-Forwarded-For"] = x_my

    # Set correct Host header for backend
    backend_host = urlparse(DESTINATION_BASE_URL).hostname
    if backend_host:
        outgoing_headers["Host"] = backend_host

    backend_url = build_backend_url(path)
    print("BACKEND URL:", backend_url)

    # Send request to backend
    resp = requests.request(
        method=method,
        url=backend_url,
        headers=outgoing_headers,
        params=query,
        data=body_bytes,
        allow_redirects=False,
    )

    # Pass all backend response headers to client, no filtering
    response_headers = dict(resp.headers)

    # Properly encode binary response data
    body_b64 = base64.b64encode(resp.content).decode("ascii")

    return {
        "statusCode": resp.status_code,
        "headers": response_headers,
        "body": body_b64,
        "isBase64Encoded": True,
    }