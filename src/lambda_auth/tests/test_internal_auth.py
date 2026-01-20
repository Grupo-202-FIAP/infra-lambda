import pytest
from unittest.mock import patch
from lambda_auth.strategies.internal_auth import InternalAuthStrategy

@pytest.fixture
def strategy():
    return InternalAuthStrategy()

@patch("lambda_auth.strategies.internal_auth.cognito_client.admin_initiate_auth")
def test_internal_auth_success(mock_auth, strategy):
    mock_auth.return_value = {
        "AuthenticationResult": {
            "IdToken": "id123",
            "AccessToken": "access123",
            "RefreshToken": "refresh123"
        }
    }

    body = {"email": "user@test.com", "password": "abc123"}
    resp = strategy.authenticate(body)

    assert resp["statusCode"] == 200
    assert "idToken" in resp["body"]

@patch("lambda_auth.strategies.internal_auth.cognito_client.admin_initiate_auth")
def test_internal_auth_missing_email(mock_auth, strategy):
    body = {"password": "123"}
    resp = strategy.authenticate(body)
    assert resp["statusCode"] == 400

@patch("lambda_auth.strategies.internal_auth.cognito_client.admin_initiate_auth")
def test_internal_auth_challenge(mock_auth, strategy):
    mock_auth.return_value = {"ChallengeName": "NEW_PASSWORD_REQUIRED", "Session": "abc"}

    body = {"email": "user@test.com", "password": "abc123"}
    resp = strategy.authenticate(body)

    assert resp["statusCode"] == 403
    assert "challenge" in resp["body"]
