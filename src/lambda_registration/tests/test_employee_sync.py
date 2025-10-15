import pytest
import os
import json
from unittest.mock import patch, MagicMock
from lambda_registration.strategies.employee_sync import EmployeeSyncStrategy

@pytest.fixture
def employee_data():
    return {
        "userId": "456",
        "email": "emp@example.com",
        "name": "Jane Doe"
    }

@patch("lambda_registration.strategies.employee_sync.DBClient")
def test_employee_sync_success(mock_db, employee_data):
    mock_instance = mock_db.return_value
    strategy = EmployeeSyncStrategy()
    result = strategy.execute(employee_data)
    mock_instance.execute.assert_called_once()
    
    body = json.loads(result["body"])
    assert result["statusCode"] == 200
    assert "Employee sincronizado" in body["message"]

def test_employee_sync_missing_fields(employee_data, mock_db_dependencies):
    strategy = EmployeeSyncStrategy()
    employee_data.pop("email")
    result = strategy.execute(employee_data)

    body = json.loads(result["body"])
    assert result["statusCode"] == 400
    assert "userId e email são obrigatórios" in body["message"]


@patch("lambda_registration.strategies.employee_sync.DBClient")
def test_employee_sync_db_exception(mock_db, employee_data):
    mock_instance = mock_db.return_value
    mock_instance.execute.side_effect = Exception("DB error")
    
    strategy = EmployeeSyncStrategy()
    result = strategy.execute(employee_data)
    
    body = json.loads(result["body"])
    assert result["statusCode"] == 500
    assert "Erro ao sincronizar employee" in body["message"]
