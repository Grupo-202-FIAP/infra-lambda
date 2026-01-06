import pytest
import os
import json
from unittest.mock import patch, MagicMock
from lambda_registration.strategies.internal_sync import InternalSyncStrategy

@pytest.fixture
def internal_data():
    return {
        "userId": "456",
        "email": "internal@example.com",
        "name": "Jane Doe"
    }

@patch("lambda_registration.strategies.internal_sync.DBClient")
def test_internal_sync_success(mock_db, internal_data):
    mock_instance = mock_db.return_value
    strategy = InternalSyncStrategy()
    result = strategy.execute(internal_data)
    mock_instance.execute.assert_called_once()
    
    body = json.loads(result["body"])
    assert result["statusCode"] == 200
    assert "Interno sincronizado" in body["message"]

def test_internal_sync_missing_fields(internal_data, mock_db_dependencies):
    strategy = InternalSyncStrategy()
    internal_data.pop("email")
    result = strategy.execute(internal_data)

    body = json.loads(result["body"])
    assert result["statusCode"] == 400
    assert "userId e email são obrigatórios" in body["message"]


@patch("lambda_registration.strategies.internal_sync.DBClient")
def test_internal_sync_db_exception(mock_db, internal_data):
    mock_instance = mock_db.return_value
    mock_instance.execute.side_effect = Exception("DB error")
    
    strategy = InternalSyncStrategy()
    result = strategy.execute(internal_data)
    
    body = json.loads(result["body"])
    assert result["statusCode"] == 500
    assert "Erro ao sincronizar interno" in body["message"]

