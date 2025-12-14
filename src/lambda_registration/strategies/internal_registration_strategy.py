import os
import json
import boto3
import logging
from botocore.exceptions import ClientError
from ..utils.responses import response

logger = logging.getLogger()
logger.setLevel(logging.INFO)

REGION = os.environ.get("REGION", "us-east-1")
SQS_QUEUE_URL = os.environ.get("SQS_QUEUE_URL")

sqs_client = boto3.client("sqs", region_name=REGION)


class InternalRegistrationStrategy:

    def execute(self, data):
        logger.info(f"[InternalRegistration] Iniciando execução com dados: {data}")

        email = data.get("email")
        password = data.get("password")
        name = data.get("name")

        if not email or not password:
            logger.warning("[InternalRegistration] Campos obrigatórios ausentes: email e/ou password.")
            return response(400, {"message": "Obrigatório enviar email e password"})

        if not SQS_QUEUE_URL:
            logger.error("[InternalRegistration] SQS_QUEUE_URL não configurada nas variáveis de ambiente")
            return response(500, {"message": "Configuração SQS não encontrada"})

        try:
            logger.info(f"[InternalRegistration] Publicando mensagem no SQS para email={email}")
            
            # Preparar mensagem para o SQS
            message_body = {
                "type": "internal",
                "action": "register",
                "data": {
                    "email": email,
                    "password": password,
                    "name": name,
                    "user_attributes": [
                        {"Name": "email", "Value": email},
                        {"Name": "email_verified", "Value": "true"},
                    ]
                }
            }
            
            # Adicionar name aos atributos se fornecido
            if name:
                message_body["data"]["user_attributes"].append({"Name": "name", "Value": name})

            # Publicar mensagem no SQS
            response_sqs = sqs_client.send_message(
                QueueUrl=SQS_QUEUE_URL,
                MessageBody=json.dumps(message_body),
                MessageAttributes={
                    "type": {
                        "StringValue": "internal",
                        "DataType": "String"
                    },
                    "action": {
                        "StringValue": "register",
                        "DataType": "String"
                    },
                    "email": {
                        "StringValue": email,
                        "DataType": "String"
                    }
                }
            )

            message_id = response_sqs.get("MessageId")
            logger.info(f"[InternalRegistration] Mensagem publicada no SQS com sucesso. MessageId={message_id}")

            return response(201, {
                "message": "Solicitação de registro de usuário interno enviada para processamento",
                "messageId": message_id,
                "queueUrl": SQS_QUEUE_URL
            })

        except ClientError as e:
            logger.exception(f"[InternalRegistration] Erro SQS ao publicar mensagem email={email}: {e}")
            return response(500, {"message": f"Erro ao publicar no SQS: {e}"})

        except Exception as e:
            logger.exception(f"[InternalRegistration] Erro inesperado: {e}")
            return response(500, {"message": f"Erro interno: {e}"})
