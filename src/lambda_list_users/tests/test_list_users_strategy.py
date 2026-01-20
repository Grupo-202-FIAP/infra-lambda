import json
from unittest.mock import MagicMock
from lambda_list_users.strategies.list_users_strategy import ListUsersStrategy


def test_list_users_success():
    mock_db = MagicMock()
    # count query returns total=2
    mock_db.fetch_one.return_value = {"total": 2}
    # list query returns two mixed users
    mock_db.fetch_all.return_value = [
        {
            "type": "customer",
            "id": "c1",
            "cognito_user_id": "cg1",
            "cpf": "00011122233",
            "email": "cust@example.com",
            "name": "Customer One",
            "status": "active",
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2025-01-02T00:00:00Z",
        },
        {
            "type": "internal",
            "id": "i1",
            "cognito_user_id": "cg2",
            "cpf": None,
            "email": "internal@example.com",
            "name": "Internal One",
            "status": None,
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2025-01-02T00:00:00Z",
        },
    ]

    strategy = ListUsersStrategy(db_client=mock_db)
    result = strategy.execute({"page": 1, "per_page": 10, "email": "example"})

    assert result["statusCode"] == 200
    body = json.loads(result["body"]) 
    assert body["message"] == "Usuários listados com sucesso"
    assert len(body["users"]) == 2
    assert body["pagination"]["total_records"] == 2
    assert body["pagination"]["page"] == 1


def test_list_users_invalid_pagination():
    mock_db = MagicMock()
    strategy = ListUsersStrategy(db_client=mock_db)

    result = strategy.execute({"page": "abc", "per_page": "xyz"})

    assert result["statusCode"] == 400
    body = json.loads(result["body"]) 
    assert "paginação inválidos" in body["message"]
