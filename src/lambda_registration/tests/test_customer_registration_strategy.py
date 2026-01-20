import os
import json
import pytest

from lambda_registration.utils.responses import response
from lambda_registration.strategies.customer_registration_strategy import CustomerRegistrationStrategy

class FakeCognitoClient:
    """Mock simples para CognitoClient"""
    def __init__(self):
        self.users = {}

    def get_user_by_username(self, user_pool_id, username):
        return self.users.get(username)

    def admin_create_user(self, user_pool_id, username, user_attributes, message_action=None, **kwargs):
        if username in self.users:
            raise Exception("Usuário já existe (mock)")
        self.users[username] = {"User": {"Username": username}}
        return {"User": {"Username": username}}


@pytest.fixture
def fake_cognito():
    return FakeCognitoClient()


def test_customer_registration_success(fake_cognito):
    strategy = CustomerRegistrationStrategy(cognito=fake_cognito)
    data = {"cpf": "12345678900"}

    result = strategy.execute(data)
    body = json.loads(result["body"])

    assert result["statusCode"] == 201
    assert "Cliente cadastrado com sucesso" in body["message"]
    assert "userId" in body


def test_customer_registration_conflict(fake_cognito):
    fake_cognito.users["12345678900"] = {"User": {"Username": "12345678900"}}
    strategy = CustomerRegistrationStrategy(cognito=fake_cognito)

    result = strategy.execute({"cpf": "12345678900"})
    body = json.loads(result["body"])

    assert result["statusCode"] == 409
    assert "Cliente já cadastrado" in body["message"]


def test_customer_registration_missing_cpf(fake_cognito):
    strategy = CustomerRegistrationStrategy(cognito=fake_cognito)
    result = strategy.execute({})
    body = json.loads(result["body"])

    assert result["statusCode"] == 400
    assert "Obrigatório enviar CPF" in body["message"]