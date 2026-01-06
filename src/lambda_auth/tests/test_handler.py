import json
import pytest
from handler import handler

def test_handler_missing_type():
    event = {"body": json.dumps({})}
    resp = handler(event, None)
    assert resp["statusCode"] == 400
    assert "type" in resp["body"]

def test_handler_invalid_type():
    event = {"body": json.dumps({"type": "invalid"})}
    resp = handler(event, None)
    assert resp["statusCode"] == 400
    body = json.loads(resp["body"])
    assert "não suportado" in body["message"]
