import pytest
import os
import json
from unittest.mock import patch, MagicMock
from lambda_registration.strategies.customer_sync import CustomerSyncStrategy

@pytest.fixture
def customer_data():
    return {
        "userId": "123",
        "cpf": "00011122233",
        "email": "test@example.com",
        "name": "John Doe"
    }

@patch("lambda_registration.strategies.customer_sync.DBClient")
def test_customer_sync_success(mock_db, customer_data):
    mock_instance = mock_db.return_value
    strategy = CustomerSyncStrategy()
    result = strategy.execute(customer_data)
    mock_instance.execute.assert_called_once()
    
    body = json.loads(result["body"])
    assert result["statusCode"] == 200
    assert "Customer sincronizado" in body["message"]

def test_customer_sync_missing_userid(customer_data, mock_db_dependencies):
    strategy = CustomerSyncStrategy()
    customer_data.pop("userId")
    result = strategy.execute(customer_data)

    body = json.loads(result["body"])
    assert result["statusCode"] == 400
    assert "userId obrigatório" in body["message"]


@patch("lambda_registration.strategies.customer_sync.DBClient")
def test_customer_sync_db_exception(mock_db, customer_data):
    mock_instance = mock_db.return_value
    mock_instance.execute.side_effect = Exception("DB error")
    
    strategy = CustomerSyncStrategy()
    result = strategy.execute(customer_data)
    
    body = json.loads(result["body"])
    assert result["statusCode"] == 500
    assert "Erro ao sincronizar customer" in body["message"]
