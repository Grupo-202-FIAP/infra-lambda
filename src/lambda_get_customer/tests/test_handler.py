import pytest
import json
from unittest.mock import patch, MagicMock
from lambda_get_customer.handler import handler


@pytest.fixture
def api_gateway_event_with_query_params():
    """Simula evento do API Gateway com queryStringParameters (GET request)"""
    return {
        "queryStringParameters": {
            "customer_id": "123"
        },
        "body": None
    }


@pytest.fixture
def api_gateway_event_with_body():
    """Simula evento do API Gateway com body (POST request)"""
    return {
        "queryStringParameters": None,
        "body": json.dumps({
            "email": "test@example.com"
        })
    }


@pytest.fixture
def api_gateway_event_no_params():
    """Simula evento sem parâmetros"""
    return {
        "queryStringParameters": None,
        "body": "{}"
    }


@pytest.fixture
def api_gateway_event_invalid_json():
    """Simula evento com JSON inválido"""
    return {
        "queryStringParameters": None,
        "body": "invalid json {"
    }


@patch("lambda_get_customer.handler.GetCustomerStrategy")
def test_handler_with_query_params_success(mock_strategy, api_gateway_event_with_query_params):
    """Testa handler com query parameters (GET request)"""
    mock_instance = mock_strategy.return_value
    mock_instance.execute.return_value = {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Cliente encontrado com sucesso",
            "customer": {"id": "123", "email": "test@example.com"}
        })
    }
    
    result = handler(api_gateway_event_with_query_params, None)
    
    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert body["message"] == "Cliente encontrado com sucesso"
    assert body["customer"]["id"] == "123"
    mock_instance.execute.assert_called_once()


@patch("lambda_get_customer.handler.GetCustomerStrategy")
def test_handler_with_body_success(mock_strategy, api_gateway_event_with_body):
    """Testa handler com body (POST request)"""
    mock_instance = mock_strategy.return_value
    mock_instance.execute.return_value = {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Cliente encontrado com sucesso",
            "customer": {"id": "123", "email": "test@example.com"}
        })
    }
    
    result = handler(api_gateway_event_with_body, None)
    
    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert body["customer"]["email"] == "test@example.com"


@patch("lambda_get_customer.handler.GetCustomerStrategy")
def test_handler_customer_not_found(mock_strategy, api_gateway_event_with_query_params):
    """Testa handler quando cliente não é encontrado"""
    mock_instance = mock_strategy.return_value
    mock_instance.execute.return_value = {
        "statusCode": 404,
        "body": json.dumps({
            "message": "Cliente não encontrado"
        })
    }
    
    result = handler(api_gateway_event_with_query_params, None)
    
    assert result["statusCode"] == 404
    body = json.loads(result["body"])
    assert body["message"] == "Cliente não encontrado"


def test_handler_no_params(api_gateway_event_no_params):
    """Testa handler sem parâmetros de busca"""
    result = handler(api_gateway_event_no_params, None)
    
    assert result["statusCode"] == 400
    body = json.loads(result["body"])
    assert "pelo menos um parâmetro de busca" in body["message"]


def test_handler_invalid_json(api_gateway_event_invalid_json):
    """Testa handler com JSON inválido no body"""
    result = handler(api_gateway_event_invalid_json, None)
    
    assert result["statusCode"] == 400
    body = json.loads(result["body"])
    assert "inválido" in body["message"]


@patch("lambda_get_customer.handler.GetCustomerStrategy")
def test_handler_internal_error(mock_strategy, api_gateway_event_with_query_params):
    """Testa handler com erro interno inesperado"""
    mock_instance = mock_strategy.return_value
    mock_instance.execute.side_effect = Exception("Unexpected error")
    
    result = handler(api_gateway_event_with_query_params, None)
    
    assert result["statusCode"] == 500
    body = json.loads(result["body"])
    assert "Erro interno do servidor" in body["message"]


@patch("lambda_get_customer.handler.GetCustomerStrategy")
def test_handler_validation_error(mock_strategy, api_gateway_event_with_query_params):
    """Testa handler com erro de validação"""
    mock_instance = mock_strategy.return_value
    mock_instance.execute.side_effect = ValueError("Invalid parameter")
    
    result = handler(api_gateway_event_with_query_params, None)
    
    assert result["statusCode"] == 400
    body = json.loads(result["body"])
    assert "Invalid parameter" in body["message"]


@patch("lambda_get_customer.handler.GetCustomerStrategy")
def test_handler_with_multiple_search_params(mock_strategy):
    """Testa handler com múltiplos parâmetros de busca"""
    mock_instance = mock_strategy.return_value
    mock_instance.execute.return_value = {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Cliente encontrado com sucesso",
            "customer": {"id": "123", "email": "test@example.com", "cpf": "00011122233"}
        })
    }
    
    event = {
        "queryStringParameters": {
            "customer_id": "123",
            "email": "test@example.com",
            "cpf": "00011122233"
        },
        "body": None
    }
    
    result = handler(event, None)
    
    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert body["customer"]["id"] == "123"
    assert body["customer"]["email"] == "test@example.com"
