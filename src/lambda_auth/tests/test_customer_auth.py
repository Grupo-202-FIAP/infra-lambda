import pytest
import jwt
import os
import json
from unittest.mock import patch
from strategies.customer_auth import CustomerAuthStrategy


@pytest.fixture
def strategy():
    return CustomerAuthStrategy()

@patch("strategies.customer_auth.cognito_client.list_users")
def test_customer_auth_success(mock_list, strategy):
    mock_list.return_value = {"Users": [{"Username": "12345678900"}]}
    body = {"cpf": "12345678900"}
    resp = strategy.authenticate(body)

    assert resp["statusCode"] == 200
    assert "token" in resp["body"]

    data = jwt.decode(
        json.loads(resp["body"])["token"],
        os.environ.get("JWT_SECRET", "TESTE_SECRET"),
        algorithms=["HS256"]
    )
    assert data["role"] == "ROLE_CUSTOMER"

@patch("strategies.customer_auth.cognito_client.list_users")
def test_customer_auth_not_found(mock_list, strategy):
    mock_list.return_value = {"Users": []}
    body = {"cpf": "99999999999"}
    resp = strategy.authenticate(body)
    assert resp["statusCode"] == 404

def test_customer_auth_missing_cpf(strategy):
    resp = strategy.authenticate({})
    assert resp["statusCode"] == 400
