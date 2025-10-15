import os
import json
import pytest
from unittest.mock import patch, MagicMock

from lambda_registration.strategies.customer_sync import CustomerSyncStrategy
from lambda_registration.strategies.employee_sync import EmployeeSyncStrategy
from lambda_registration.utils.responses import response
from lambda_registration.strategies.employee_registration_strategy import EmployeeRegistrationStrategy
from lambda_registration.strategies.customer_registration_strategy import CustomerRegistrationStrategy

class FakeCognitoClient:
    """Mock de CognitoClient"""
    def __init__(self):
        self.created_users = {}
        self.auth_calls = []

    def admin_create_user(self, user_pool_id, username, user_attributes, temporary_password=None, message_action=None):
        self.created_users[username] = {
            "User": {"Username": username},
            "Attributes": user_attributes,
            "Password": temporary_password
        }
        return {"User": {"Username": username}}

    def admin_initiate_auth(self, user_pool_id, client_id, auth_flow, auth_parameters):
        self.auth_calls.append(auth_parameters)
        return {"ChallengeName": "NEW_PASSWORD_REQUIRED"}

    def get_user_by_username(self, user_pool_id, username):
        return self.created_users.get(username)


@pytest.fixture
def fake_cognito():
    return FakeCognitoClient()


def test_employee_registration_success(fake_cognito):
    strategy = EmployeeRegistrationStrategy(cognito=fake_cognito)
    data = {"email": "user@test.com", "password": "Pass@123", "name": "João"}

    result = strategy.execute(data)
    body = json.loads(result["body"])

    assert result["statusCode"] == 201
    assert "Usuário interno cadastrado com sucesso" in body["message"]
    assert "challenge" in body
    assert "username" in body


def test_employee_registration_missing_fields(fake_cognito):
    strategy = EmployeeRegistrationStrategy(cognito=fake_cognito)
    result = strategy.execute({"email": "user@test.com"})
    body = json.loads(result["body"])

    assert result["statusCode"] == 400
    assert "Obrigatório enviar email e password" in body["message"]


def test_customer_registration_conflict(fake_cognito):
    strategy = CustomerRegistrationStrategy(cognito=fake_cognito)
    fake_cognito.created_users["12345678900"] = {"User": {"Username": "12345678900"}}
    data = {"cpf": "12345678900", "email": "test@example.com", "name": "John Doe"}

    result = strategy.execute(data)
    body = json.loads(result["body"])

    assert result["statusCode"] == 409
    assert "Cliente já cadastrado" in body["message"]


def test_customer_registration_missing_cpf(fake_cognito):
    strategy = CustomerRegistrationStrategy(cognito=fake_cognito)
    result = strategy.execute({})
    body = json.loads(result["body"])

    assert result["statusCode"] == 400
    assert "Obrigatório enviar CPF" in body["message"]