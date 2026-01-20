import pytest
import json
from unittest.mock import patch, MagicMock
from lambda_get_user.strategies.get_user_strategy import GetUserStrategy


@pytest.fixture
def user_search_by_id():
    return {"user_id": "123"}


@pytest.fixture
def user_search_by_email():
    return {"email": "test@example.com"}


@pytest.fixture
def user_search_by_cpf():
    return {"cpf": "00011122233"}


@pytest.fixture
def mock_customer_data():
    return {
        "id": "123",
        "cognito_user_id": "cognito-123",
        "cpf": "00011122233",
        "email": "test@example.com",
        "name": "John Doe"
    }


@pytest.fixture
def mock_internal_data():
    return {
        "id": "999",
        "cognito_user_id": "cognito-999",
        "email": "internal@example.com",
        "name": "Jane Admin"
    }


@patch("lambda_get_user.strategies.get_user_strategy.DBClient")
def test_get_user_by_id_customer_success(mock_db, user_search_by_id, mock_customer_data):
    mock_instance = mock_db.return_value
    # first query (customers) returns data
    mock_instance.fetch_one.return_value = mock_customer_data

    strategy = GetUserStrategy(db_client=mock_instance)
    result = strategy.execute(user_search_by_id)

    body = json.loads(result["body"]) 
    assert result["statusCode"] == 200
    assert body["message"] == "Usuário encontrado com sucesso"
    assert body["user"]["id"] == "123"
    assert body["user"]["type"] == "customer"


@patch("lambda_get_user.strategies.get_user_strategy.DBClient")
def test_get_user_by_email_internal_success(mock_db, user_search_by_email, mock_internal_data):
    mock_instance = mock_db.return_value
    # first customers query returns None, then internal returns data
    mock_instance.fetch_one.side_effect = [None, mock_internal_data]

    strategy = GetUserStrategy(db_client=mock_instance)
    result = strategy.execute(user_search_by_email)

    body = json.loads(result["body"]) 
    assert result["statusCode"] == 200
    assert body["user"]["email"] == "internal@example.com"
    assert body["user"]["type"] == "internal"


@patch("lambda_get_user.strategies.get_user_strategy.DBClient")
def test_get_user_by_cpf_success(mock_db, user_search_by_cpf, mock_customer_data):
    mock_instance = mock_db.return_value
    mock_instance.fetch_one.return_value = mock_customer_data

    strategy = GetUserStrategy(db_client=mock_instance)
    result = strategy.execute(user_search_by_cpf)

    body = json.loads(result["body"]) 
    assert result["statusCode"] == 200
    assert body["user"]["cpf"] == "00011122233"
    assert body["user"]["type"] == "customer"


@patch("lambda_get_user.strategies.get_user_strategy.DBClient")
def test_get_user_not_found(mock_db, user_search_by_id):
    mock_instance = mock_db.return_value
    mock_instance.fetch_one.return_value = None

    strategy = GetUserStrategy(db_client=mock_instance)
    result = strategy.execute(user_search_by_id)

    body = json.loads(result["body"]) 
    assert result["statusCode"] == 404
    assert body["message"] == "Usuário não encontrado"


@patch("lambda_get_user.strategies.get_user_strategy.DBClient")
def test_get_user_no_params(mock_db):
    mock_instance = mock_db.return_value
    strategy = GetUserStrategy(db_client=mock_instance)
    result = strategy.execute({})
    body = json.loads(result["body"]) 
    assert result["statusCode"] == 400
    assert "pelo menos um parâmetro de busca" in body["message"]


@patch("lambda_get_user.strategies.get_user_strategy.DBClient")
def test_get_user_removes_sensitive_data(mock_db):
    mock_instance = mock_db.return_value
    user_with_password = {
        "id": "123",
        "email": "test@example.com",
        "password": "secret123",
        "name": "John Doe"
    }
    mock_instance.fetch_one.return_value = user_with_password

    strategy = GetUserStrategy(db_client=mock_instance)
    result = strategy.execute({"user_id": "123"})

    body = json.loads(result["body"]) 
    assert result["statusCode"] == 200
    assert "password" not in body["user"]
    assert body["user"]["email"] == "test@example.com"
