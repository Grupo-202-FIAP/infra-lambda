import os
import json
import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture(autouse=True)
def set_env():
    # Garantir variáveis de DB para evitar falha no __init__ do DBClient
    os.environ.setdefault("DB_HOST", "localhost:5432")
    os.environ.setdefault("DB_USER", "user")
    os.environ.setdefault("DB_PASSWORD", "pass")
    os.environ.setdefault("DB_NAME", "testdb")
    os.environ.setdefault("REGION", "us-east-1")

@pytest.fixture
def mock_db_dependencies():
    # Mockar conexão psycopg2 para evitar acesso real ao banco
    with patch("lambda_registration.utils.db_client.psycopg2.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        yield mock_conn

class FakeCognitoClient:
    """Mock simples para CognitoClient, compartilhado entre testes."""
    def __init__(self):
        self.created_users = {}

    def get_user_by_username(self, user_pool_id, username):
        return self.created_users.get(username)

    def admin_create_user(self, user_pool_id, username, user_attributes, temporary_password=None, message_action=None, **kwargs):
        if username in self.created_users:
            raise Exception("Usuário já existe (mock)")
        self.created_users[username] = {"User": {"Username": username}}
        return {"User": {"Username": username}}

@pytest.fixture
def fake_cognito():
    return FakeCognitoClient()