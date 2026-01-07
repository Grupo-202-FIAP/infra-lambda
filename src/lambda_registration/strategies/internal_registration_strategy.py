import os
import json
import logging
import boto3
from botocore.exceptions import ClientError
from ..utils.responses import response
from ..utils.cognito_client import CognitoClient

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Cliente SQS em nível de módulo para facilitar mocking nos testes
sqs_client = boto3.client("sqs", region_name=os.getenv("REGION", os.getenv("AWS_REGION", "us-east-1")))

class InternalRegistrationStrategy:
    def __init__(self, cognito: CognitoClient = None):
        self.cognito = cognito or CognitoClient()
        self.user_pool_id = os.getenv("INTERNAL_USER_POOL_ID")
        logger.info(f"[InternalRegistrationStrategy] Inicializado com USER_POOL_ID={self.user_pool_id}")

    def execute(self, data):
        logger.info(f"[InternalRegistration] Iniciando execução com dados: {data}")

        email = data.get("email")
        password = data.get("password")
        name = data.get("name")

        if not email or not password:
            logger.warning("[InternalRegistration] Campos obrigatórios ausentes: email e/ou password.")
            return response(400, {"message": "Obrigatório enviar email e password"})

        # Encaminhar solicitação para fila SQS para processamento assíncrono
        queue_url = os.getenv("SQS_QUEUE_URL")
        if not queue_url:
            logger.error("[InternalRegistration] Configuração SQS não encontrada (SQS_QUEUE_URL)")
            return response(500, {"message": "Configuração SQS não encontrada"})

        message = {
            "type": "internal",
            "action": "register",
            "data": {
                "email": email,
                "password": password,
                "name": name
            }
        }

        try:
            logger.info("[InternalRegistration] Enviando mensagem para fila SQS")
            resp = sqs_client.send_message(
                QueueUrl=queue_url,
                MessageBody=json.dumps(message, ensure_ascii=False)
            )
            logger.info(f"[InternalRegistration] Mensagem enviada com sucesso: MessageId={resp.get('MessageId')}")

            return response(201, {
                "message": "Solicitação de registro de usuário interno enviada para processamento",
                "messageId": resp.get("MessageId"),
                "queueUrl": queue_url
            })
        except Exception as e:
            logger.exception(f"[InternalRegistration] Erro ao enviar mensagem para SQS: {e}")
            return response(500, {"message": f"Erro ao enfileirar solicitação: {e}"})
