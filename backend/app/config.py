from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str = "postgres"
    postgres_port: int = 5432

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_days: int = 7

    keycloak_server_url: str
    keycloak_public_url: str
    keycloak_realm: str
    keycloak_client_id: str
    keycloak_client_secret: str

    frontend_url: str = "http://localhost:5173"

    # Test mode - disables authentication
    disable_auth: bool = False

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    @property
    def keycloak_token_url(self) -> str:
        return f"{self.keycloak_server_url}/realms/{self.keycloak_realm}/protocol/openid-connect/token"

    @property
    def keycloak_userinfo_url(self) -> str:
        return f"{self.keycloak_server_url}/realms/{self.keycloak_realm}/protocol/openid-connect/userinfo"

    @property
    def keycloak_authorization_url(self) -> str:
        return f"{self.keycloak_public_url}/realms/{self.keycloak_realm}/protocol/openid-connect/auth"

    @property
    def keycloak_logout_url(self) -> str:
        return f"{self.keycloak_public_url}/realms/{self.keycloak_realm}/protocol/openid-connect/logout"

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
