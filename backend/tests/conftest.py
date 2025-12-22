import os
import pytest

def pytest_configure(config):
    """Set up environment variables before pytest starts collecting tests"""
    os.environ["POSTGRES_USER"] = "test"
    os.environ["POSTGRES_PASSWORD"] = "test"
    os.environ["POSTGRES_DB"] = "test"
    os.environ["POSTGRES_HOST"] = "localhost"
    os.environ["POSTGRES_PORT"] = "5432"
    os.environ["SECRET_KEY"] = "test_secret_key_for_unit_tests"
    os.environ["JWT_ISSUER"] = "test-issuer"
    os.environ["KEYCLOAK_SERVER_URL"] = "http://localhost:8080"
    os.environ["KEYCLOAK_PUBLIC_URL"] = "http://localhost:8080"
    os.environ["KEYCLOAK_REALM"] = "test"
    os.environ["KEYCLOAK_CLIENT_ID"] = "test"
    os.environ["KEYCLOAK_CLIENT_SECRET"] = "test"
    os.environ["FRONTEND_URL"] = "http://localhost"
    os.environ["DISABLE_AUTH"] = "false"
