import os
import json
import logging
import boto3
from botocore.exceptions import ClientError
from ..utils.responses import response
from ..utils.cognito_client import CognitoClient
from ..utils.db_client import DBClient

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Cliente SQS em nível de módulo para facilitar mocking nos testes
sqs_client = boto3.client("sqs", region_name=os.getenv("REGION", os.getenv("AWS_REGION", "us-east-1")))

class InternalRegistrationStrategy:
    def __init__(self, cognito: CognitoClient = None, db_client: DBClient = None):
        self.cognito = cognito or CognitoClient()
        self.db = db_client or DBClient()
        self.user_pool_id = os.getenv("INTERNAL_USER_POOL_ID")
        self.table_name = os.getenv("INTERNAL_TABLE", "internal_users")
        logger.info(f"[InternalRegistrationStrategy] Inicializado com USER_POOL_ID={self.user_pool_id}")

    def execute(self, data):
        logger.info(f"[InternalRegistration] Iniciando execução com dados: {data}")

        email = data.get("email")
        password = data.get("password")
        name = data.get("name")

        if not email or not password:
            logger.warning("[InternalRegistration] Campos obrigatórios ausentes: email e/ou password.")
            return response(400, {"message": "Obrigatório enviar email e password"})

        try:
            logger.info(f"[InternalRegistration] Verificando existência do usuário com email={email}")
            existing = self.cognito.get_user_by_username(self.user_pool_id, email)

            if existing:
                logger.info(f"[InternalRegistration] Usuário com email={email} já cadastrado no Cognito.")
                return response(409, {"message": "Usuário interno já cadastrado"})

            logger.info(f"[InternalRegistration] Criando novo usuário no Cognito com email={email}")
            user = self.cognito.admin_create_user(
                user_pool_id=self.user_pool_id,
                username=email,
                user_attributes=[
                    {"Name": "email", "Value": email},
                    {"Name": "name", "Value": name} if name else None,
                ],
                message_action="SUPPRESS"
            )

            user_id = user.get("User", {}).get("Username")
            logger.info(f"[InternalRegistration] Usuário criado no Cognito com sucesso: userId={user_id}")

            # Inserir usuário no banco de dados
            logger.info(f"[InternalRegistration] Inserindo usuário no banco de dados")
            query = (
                f"INSERT INTO {self.table_name} (cognito_user_id, email, name) "
                "VALUES (%s, %s, %s) "
                "ON CONFLICT DO NOTHING"
            )
            self.db.execute(query, (user_id, email, name))
            logger.info(f"[InternalRegistration] Usuário inserido no banco de dados com sucesso")

            return response(201, {
                "message": "Usuário interno cadastrado com sucesso",
                "userId": user_id
            })
        except Exception as e:
            logger.exception(f"[InternalRegistration] Erro ao processar registro interno: {e}")
            return response(500, {"message": "Erro interno ao processar solicitação"})
