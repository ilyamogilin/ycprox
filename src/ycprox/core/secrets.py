import keyring
from keyring.backend import KeyringBackend
from ycprox.core.config import settings
from enum import Enum


class TestKeyring(KeyringBackend):
    priority = 1
    storage = {}

    def set_password(self, service, username, password):
        self.storage[(service, username)] = password

    def get_password(self, service, username):
        return self.storage.get((service, username))

    def delete_password(self, service, username):
        self.storage.pop((service, username), None)


assert settings.debug, "Debug mode must be enabled"
keyring.set_keyring(TestKeyring())

class SecretsNames(Enum):
    CLI_NAME = "ycprox"
    OAUTH = "oauth_yandex_token"

class Vault():
    def get_oauth_token(self):
        return keyring.get_password(SecretsNames.CLI_NAME, SecretsNames.OAUTH)

    def set_oauth_token(self, token):
        keyring.set_password(SecretsNames.CLI_NAME, SecretsNames.OAUTH, token)
    
    def delete_oauth_token(self):
        keyring.delete_password(SecretsNames.CLI_NAME, SecretsNames.OAUTH)

vault = Vault()