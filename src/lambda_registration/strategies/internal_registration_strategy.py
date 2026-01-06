import os
import logging
from botocore.exceptions import ClientError
from ..utils.responses import response
from ..utils.cognito_client import CognitoClient

logger = logging.getLogger()
logger.setLevel(logging.INFO)

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

        try:
            logger.info(f"[InternalRegistration] Verificando existência do usuário com email={email}")
            existing = self.cognito.get_user_by_username(self.user_pool_id, email)

            if existing:
                logger.info(f"[InternalRegistration] Usuário com email={email} já cadastrado no Cognito.")
                return response(409, {"message": "Usuário já cadastrado"})

            logger.info(f"[InternalRegistration] Criando novo usuário com email={email}")
            user_attributes = [
                {"Name": "email", "Value": email},
                {"Name": "email_verified", "Value": "true"}
            ]
            if name:
                user_attributes.append({"Name": "name", "Value": name})

            user = self.cognito.admin_create_user(
                user_pool_id=self.user_pool_id,
                username=email,
                user_attributes=user_attributes,
                temporary_password=password,
                message_action="SUPPRESS"
            )

            user_id = user.get("User", {}).get("Username")
            logger.info(f"[InternalRegistration] Usuário criado com sucesso: userId={user_id}")

            return response(201, {
                "message": "Usuário cadastrado com sucesso",
                "userId": user_id
            })

        except ClientError as e:
            logger.exception(f"[InternalRegistration] Erro Cognito ao criar usuário email={email}: {e}")
            return response(500, {"message": f"Erro Cognito: {e}"})

        except Exception as e:
            logger.exception(f"[InternalRegistration] Erro inesperado: {e}")
            return response(500, {"message": f"Erro interno: {e}"})
