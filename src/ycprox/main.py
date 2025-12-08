from ycprox.core.secrets import vault
from ycprox.cli import Application
from pydantic_settings import CliApp
from ycprox.helpers.apispec import API_SPEC

def main():
    CliApp.run(Application)

def test_vault():
    vault.save_oauth_token("1234567890")
    token = vault.load_oauth_token()
    if token:
        print(f"Token is {token}")
    else:
        print("Token not found")
    vault.remove_oauth_token()
    token = vault.load_oauth_token()
    if token:
        print(f"Token is {token}")
    else:
        print("Token not found")

def test_api_gateway_spec():
    print(API_SPEC.format(version="1.0.0", function_id="d4eo19j12tiqo3oe1jca"))

if __name__ == "__main__":
    main()