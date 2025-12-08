API_SPEC = """openapi: 3.0.0
info:
  title: ycprox gateway to cloud function
  version: {version}

paths:
  /:
    x-yc-apigateway-any-method:
      summary: Root path, proxied through Cloud Function
      parameters:
        - name: X-My-X-Forwarded-For
          in: header
          required: false
          schema:
            type: string
      x-yc-apigateway-integration:
        type: cloud_functions
        function_id: {function_id}
        tag: "$latest"
        payload:
          path: "/"
          method: "{{httpMethod}}"
          headers: "{{headers}}"
          query: "{{query}}"
          body: "{{body}}"
          isBase64Encoded: "{{isBase64Encoded}}"
      responses:
        "200":
          description: Proxied response

  /{{proxy+}}:
    x-yc-apigateway-any-method:
      summary: Catch-all proxy via Cloud Function
      parameters:
        - name: proxy
          in: path
          required: true
          schema:
            type: string
        - name: X-My-X-Forwarded-For
          in: header
          required: false
          schema:
            type: string

      x-yc-apigateway-integration:
        type: cloud_functions
        function_id: {function_id}
        tag: "$latest"
        payload:
          path: "/{{proxy}}"
          method: "{{httpMethod}}"
          headers: "{{headers}}"
          query: "{{query}}"
          body: "{{body}}"
          isBase64Encoded: "{{isBase64Encoded}}"
      responses:
        "200":
          description: Proxied response"""