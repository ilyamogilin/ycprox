from ycprox.core.secrets import vault
from ycprox.cli.auth import Application
from pydantic_settings import CliApp

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

if __name__ == "__main__":
    main()