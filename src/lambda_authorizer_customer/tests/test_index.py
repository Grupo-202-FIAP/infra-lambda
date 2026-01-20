import json
from src import index

def test_handler_cpf(monkeypatch):
    event = {"body": json.dumps({"cpf": "12345678901"})}
    context = None

    def fake_list_users(UserPoolId, Filter, Limit):
        return {"Users": [{"Username": "12345678901"}]}

    monkeypatch.setattr(index.cognito_client, "list_users", fake_list_users)

    response = index.handler(event, context)
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert "token" in body
