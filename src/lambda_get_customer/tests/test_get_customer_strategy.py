import pytest
import json
from unittest.mock import patch, MagicMock
from lambda_get_customer.strategies.get_customer_strategy import GetCustomerStrategy


@pytest.fixture
def customer_search_by_id():
    return {"customer_id": "123"}


@pytest.fixture
def customer_search_by_email():
    return {"email": "test@example.com"}


@pytest.fixture
def customer_search_by_cpf():
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


@patch("lambda_get_customer.strategies.get_customer_strategy.DBClient")
def test_get_customer_by_id_success(mock_db, customer_search_by_id, mock_customer_data):
    """Testa busca de cliente por ID com sucesso"""
    mock_instance = mock_db.return_value
    mock_instance.fetch_one.return_value = mock_customer_data
    
    strategy = GetCustomerStrategy(db_client=mock_instance)
    result = strategy.execute(customer_search_by_id)
    
    mock_instance.fetch_one.assert_called_once()
    
    body = json.loads(result["body"])
    assert result["statusCode"] == 200
    assert body["message"] == "Cliente encontrado com sucesso"
    assert body["customer"]["id"] == "123"
    assert body["customer"]["email"] == "test@example.com"


@patch("lambda_get_customer.strategies.get_customer_strategy.DBClient")
def test_get_customer_by_email_success(mock_db, customer_search_by_email, mock_customer_data):
    """Testa busca de cliente por email com sucesso"""
    mock_instance = mock_db.return_value
    mock_instance.fetch_one.return_value = mock_customer_data
    
    strategy = GetCustomerStrategy(db_client=mock_instance)
    result = strategy.execute(customer_search_by_email)
    
    mock_instance.fetch_one.assert_called_once()
    
    body = json.loads(result["body"])
    assert result["statusCode"] == 200
    assert body["customer"]["email"] == "test@example.com"


@patch("lambda_get_customer.strategies.get_customer_strategy.DBClient")
def test_get_customer_by_cpf_success(mock_db, customer_search_by_cpf, mock_customer_data):
    """Testa busca de cliente por CPF com sucesso"""
    mock_instance = mock_db.return_value
    mock_instance.fetch_one.return_value = mock_customer_data
    
    strategy = GetCustomerStrategy(db_client=mock_instance)
    result = strategy.execute(customer_search_by_cpf)
    
    mock_instance.fetch_one.assert_called_once()
    
    body = json.loads(result["body"])
    assert result["statusCode"] == 200
    assert body["customer"]["cpf"] == "00011122233"


@patch("lambda_get_customer.strategies.get_customer_strategy.DBClient")
def test_get_customer_not_found(mock_db, customer_search_by_id):
    """Testa busca de cliente que não existe (retorna 404)"""
    mock_instance = mock_db.return_value
    mock_instance.fetch_one.return_value = None
    
    strategy = GetCustomerStrategy(db_client=mock_instance)
    result = strategy.execute(customer_search_by_id)
    
    body = json.loads(result["body"])
    assert result["statusCode"] == 404
    assert body["message"] == "Cliente não encontrado"


@patch("lambda_get_customer.strategies.get_customer_strategy.DBClient")
def test_get_customer_no_params(mock_db):
    """Testa busca sem parâmetros (retorna 400)"""
    mock_instance = mock_db.return_value
    
    strategy = GetCustomerStrategy(db_client=mock_instance)
    result = strategy.execute({})
    
    body = json.loads(result["body"])
    assert result["statusCode"] == 400
    assert "pelo menos um parâmetro de busca" in body["message"]


@patch("lambda_get_customer.strategies.get_customer_strategy.DBClient")
def test_get_customer_db_exception(mock_db, customer_search_by_id):
    """Testa erro de banco de dados (retorna 500)"""
    mock_instance = mock_db.return_value
    mock_instance.fetch_one.side_effect = Exception("Database connection error")
    
    strategy = GetCustomerStrategy(db_client=mock_instance)
    result = strategy.execute(customer_search_by_id)
    
    body = json.loads(result["body"])
    assert result["statusCode"] == 500
    assert "Erro interno ao buscar cliente" in body["message"]


@patch("lambda_get_customer.strategies.get_customer_strategy.DBClient")
def test_get_customer_multiple_params(mock_db, mock_customer_data):
    """Testa busca com múltiplos parâmetros"""
    mock_instance = mock_db.return_value
    mock_instance.fetch_one.return_value = mock_customer_data
    
    search_params = {
        "customer_id": "123",
        "email": "test@example.com"
    }
    
    strategy = GetCustomerStrategy(db_client=mock_instance)
    result = strategy.execute(search_params)
    
    body = json.loads(result["body"])
    assert result["statusCode"] == 200
    assert body["customer"]["id"] == "123"


@patch("lambda_get_customer.strategies.get_customer_strategy.DBClient")
def test_get_customer_removes_sensitive_data(mock_db):
    """Testa se dados sensíveis são removidos da resposta"""
    mock_instance = mock_db.return_value
    customer_with_password = {
        "id": "123",
        "email": "test@example.com",
        "password": "secret123",
        "name": "John Doe"
    }
    mock_instance.fetch_one.return_value = customer_with_password
    
    strategy = GetCustomerStrategy(db_client=mock_instance)
    result = strategy.execute({"customer_id": "123"})
    
    body = json.loads(result["body"])
    assert result["statusCode"] == 200
    assert "password" not in body["customer"]
    assert body["customer"]["email"] == "test@example.com"
