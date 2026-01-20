import os
import json
import pytest
from unittest.mock import patch, MagicMock

from lambda_registration.strategies.customer_sync import CustomerSyncStrategy
from lambda_registration.strategies.internal_sync import InternalSyncStrategy
from lambda_registration.utils.responses import response
from lambda_registration.strategies.internal_registration_strategy import InternalRegistrationStrategy
from lambda_registration.strategies.customer_registration_strategy import CustomerRegistrationStrategy


@pytest.fixture
def mock_sqs_client():
    """Mock do cliente SQS"""
    with patch('lambda_registration.strategies.internal_registration_strategy.sqs_client') as mock_sqs:
        mock_sqs.send_message.return_value = {
            "MessageId": "test-message-id-123",
            "MD5OfMessageBody": "test-md5"
        }
        yield mock_sqs


@pytest.fixture
def set_sqs_queue_url():
    """Define a variável de ambiente SQS_QUEUE_URL"""
    os.environ["SQS_QUEUE_URL"] = "https://sqs.us-east-1.amazonaws.com/123456789012/test-queue"
    yield
    os.environ.pop("SQS_QUEUE_URL", None)


def test_internal_registration_success(mock_sqs_client, set_sqs_queue_url):
    strategy = InternalRegistrationStrategy()
    data = {"email": "user@test.com", "password": "Pass@123", "name": "João"}

    result = strategy.execute(data)
    body = json.loads(result["body"])

    assert result["statusCode"] == 201
    assert "Solicitação de registro de usuário interno enviada para processamento" in body["message"]
    assert "messageId" in body
    assert body["messageId"] == "test-message-id-123"
    assert "queueUrl" in body
    
    # Verificar se send_message foi chamado corretamente
    mock_sqs_client.send_message.assert_called_once()
    call_args = mock_sqs_client.send_message.call_args
    assert call_args.kwargs["QueueUrl"] == os.environ["SQS_QUEUE_URL"]
    
    # Verificar o conteúdo da mensagem
    message_body = json.loads(call_args.kwargs["MessageBody"])
    assert message_body["type"] == "internal"
    assert message_body["action"] == "register"
    assert message_body["data"]["email"] == "user@test.com"
    assert message_body["data"]["password"] == "Pass@123"
    assert message_body["data"]["name"] == "João"


def test_internal_registration_missing_fields(mock_sqs_client, set_sqs_queue_url):
    strategy = InternalRegistrationStrategy()
    result = strategy.execute({"email": "user@test.com"})
    body = json.loads(result["body"])

    assert result["statusCode"] == 400
    assert "Obrigatório enviar email e password" in body["message"]
    mock_sqs_client.send_message.assert_not_called()


def test_internal_registration_missing_sqs_url(mock_sqs_client):
    """Testa quando SQS_QUEUE_URL não está configurada"""
    if "SQS_QUEUE_URL" in os.environ:
        del os.environ["SQS_QUEUE_URL"]
    
    strategy = InternalRegistrationStrategy()
    data = {"email": "user@test.com", "password": "Pass@123", "name": "João"}
    
    result = strategy.execute(data)
    body = json.loads(result["body"])
    
    assert result["statusCode"] == 500
    assert "Configuração SQS não encontrada" in body["message"]
    mock_sqs_client.send_message.assert_not_called()


def test_customer_registration_conflict(fake_cognito):
    strategy = CustomerRegistrationStrategy(cognito=fake_cognito)
    fake_cognito.created_users["12345678900"] = {"User": {"Username": "12345678900"}}
    data = {"cpf": "12345678900", "email": "test@example.com", "name": "John Doe"}

    result = strategy.execute(data)
    body = json.loads(result["body"])

    assert result["statusCode"] == 409
    assert "Cliente já cadastrado" in body["message"]


def test_customer_registration_missing_cpf(fake_cognito):
    strategy = CustomerRegistrationStrategy(cognito=fake_cognito)
    result = strategy.execute({})
    body = json.loads(result["body"])

    assert result["statusCode"] == 400
    assert "Obrigatório enviar CPF" in body["message"]

