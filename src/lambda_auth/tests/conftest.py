import pytest

@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("REGION", "us-east-1")
    monkeypatch.setenv("USER_POOLS", "internal:pool123,customer:pool456")
    monkeypatch.setenv("INTERNAL_APP_CLIENT_ID", "app123")
    monkeypatch.setenv("JWT_SECRET", "TESTE_SECRET")
