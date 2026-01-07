import json
from unittest.mock import patch
from lambda_list_users.handler import handler


def test_handler_with_query_params_success():
    with patch("lambda_list_users.handler.ListUsersStrategy") as mock_strategy_cls:
        mock_strategy = mock_strategy_cls.return_value
        mock_strategy.execute.return_value = {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Usuários listados com sucesso",
                "users": [
                    {"id": "c1", "email": "cust@example.com", "type": "customer"},
                    {"id": "i1", "email": "internal@example.com", "type": "internal"},
                ],
                "pagination": {"page": 1, "per_page": 10, "total_records": 2, "total_pages": 1, "has_next": False, "has_previous": False}
            })
        }

        event = {
            "queryStringParameters": {"page": "1", "per_page": "10"},
            "body": None
        }

        result = handler(event, None)
        assert result["statusCode"] == 200
        body = json.loads(result["body"]) 
        assert body["message"] == "Usuários listados com sucesso"
        assert len(body["users"]) == 2
        mock_strategy.execute.assert_called_once()


def test_handler_invalid_json_body():
    event = {
        "queryStringParameters": None,
        "body": "{ invalid json"
    }
    result = handler(event, None)
    assert result["statusCode"] == 400
    body = json.loads(result["body"]) 
    assert "Corpo inválido" in body["message"]
