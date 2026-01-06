import pytest
import json
from unittest.mock import patch, MagicMock
from lambda_get_user.handler import handler


@pytest.fixture
def api_gateway_event_with_query_params():
    return {
        "queryStringParameters": {
            "user_id": "123"
        },
        "body": None
    }


@pytest.fixture
def api_gateway_event_with_body():
    return {
        "queryStringParameters": None,
        "body": json.dumps({
            "email": "test@example.com"
        })
    }


@pytest.fixture
def api_gateway_event_no_params():
    return {
        "queryStringParameters": None,
        "body": "{}"
    }


@pytest.fixture
def api_gateway_event_invalid_json():
    return {
        "queryStringParameters": None,
        "body": "invalid json {"
    }


@patch("lambda_get_user.handler.GetUserStrategy")
def test_handler_with_query_params_success(mock_strategy, api_gateway_event_with_query_params):
    mock_instance = mock_strategy.return_value
    mock_instance.execute.return_value = {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Usuário encontrado com sucesso",
            "user": {"id": "123", "email": "test@example.com", "type": "customer"}
        })
    }

    result = handler(api_gateway_event_with_query_params, None)

    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert body["message"] == "Usuário encontrado com sucesso"
    assert body["user"]["id"] == "123"
    mock_instance.execute.assert_called_once()


@patch("lambda_get_user.handler.GetUserStrategy")
def test_handler_with_body_success(mock_strategy, api_gateway_event_with_body):
    mock_instance = mock_strategy.return_value
    mock_instance.execute.return_value = {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Usuário encontrado com sucesso",
            "user": {"id": "123", "email": "test@example.com", "type": "internal"}
        })
    }

    result = handler(api_gateway_event_with_body, None)

    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert body["user"]["email"] == "test@example.com"


@patch("lambda_get_user.handler.GetUserStrategy")
def test_handler_user_not_found(mock_strategy, api_gateway_event_with_query_params):
    mock_instance = mock_strategy.return_value
    mock_instance.execute.return_value = {
        "statusCode": 404,
        "body": json.dumps({
            "message": "Usuário não encontrado"
        })
    }

    result = handler(api_gateway_event_with_query_params, None)

    assert result["statusCode"] == 404
    body = json.loads(result["body"]) 
    assert body["message"] == "Usuário não encontrado"


def test_handler_no_params(api_gateway_event_no_params):
    result = handler(api_gateway_event_no_params, None)

    assert result["statusCode"] == 400
    body = json.loads(result["body"]) 
    assert "pelo menos um parâmetro de busca" in body["message"]


def test_handler_invalid_json(api_gateway_event_invalid_json):
    result = handler(api_gateway_event_invalid_json, None)

    assert result["statusCode"] == 400
    body = json.loads(result["body"]) 
    assert "inválido" in body["message"]


@patch("lambda_get_user.handler.GetUserStrategy")
def test_handler_internal_error(mock_strategy, api_gateway_event_with_query_params):
    mock_instance = mock_strategy.return_value
    mock_instance.execute.side_effect = Exception("Unexpected error")

    result = handler(api_gateway_event_with_query_params, None)

    assert result["statusCode"] == 500
    body = json.loads(result["body"]) 
    assert "Erro interno do servidor" in body["message"]


@patch("lambda_get_user.handler.GetUserStrategy")
def test_handler_validation_error(mock_strategy, api_gateway_event_with_query_params):
    mock_instance = mock_strategy.return_value
    mock_instance.execute.side_effect = ValueError("Invalid parameter")

    result = handler(api_gateway_event_with_query_params, None)

    assert result["statusCode"] == 400
    body = json.loads(result["body"]) 
    assert "Invalid parameter" in body["message"]


@patch("lambda_get_user.handler.GetUserStrategy")
def test_handler_with_multiple_search_params(mock_strategy):
    mock_instance = mock_strategy.return_value
    mock_instance.execute.return_value = {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Usuário encontrado com sucesso",
            "user": {"id": "123", "email": "test@example.com", "cpf": "00011122233", "type": "customer"}
        })
    }

    event = {
        "queryStringParameters": {
            "user_id": "123",
            "email": "test@example.com",
            "cpf": "00011122233"
        },
        "body": None
    }

    result = handler(event, None)

    assert result["statusCode"] == 200
    body = json.loads(result["body"]) 
    assert body["user"]["id"] == "123"
    assert body["user"]["email"] == "test@example.com"
