API_SPEC = """
openapi: 3.0.0
info:
  title: Proxy Gateway
  version: 1.0.0
paths:
  /:
    get:
      x-yc-apigateway-integration:
        type: dummy
        http_code: 200
        content:
          application/json: '{"message": "Hello, world!"}'
      responses:
        '200':
          description: OK
"""