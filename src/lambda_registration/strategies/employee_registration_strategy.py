import os
import logging
from botocore.exceptions import ClientError
from ..utils.responses import response
from ..utils.cognito_client import CognitoClient

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class EmployeeRegistrationStrategy:
    def __init__(self, cognito: CognitoClient = None):
        self.cognito = cognito or CognitoClient()
        self.user_pool_id = os.getenv("USER_POOL_ID")
        self.app_client_id = os.getenv("INTERNAL_APP_CLIENT_ID")
        logger.info(f"[EmployeeRegistrationStrategy] Inicializado com USER_POOL_ID={self.user_pool_id}, APP_CLIENT_ID={self.app_client_id}")

    def execute(self, data):
        logger.info(f"[EmployeeRegistration] Iniciando execução com dados: {data}")

        email = data.get("email")
        password = data.get("password")
        name = data.get("name")

        if not email or not password:
            logger.warning("[EmployeeRegistration] Campos obrigatórios ausentes: email e/ou password.")
            return response(400, {"message": "Obrigatório enviar email e password"})

        try:
            logger.info(f"[EmployeeRegistration] Criando usuário interno com email={email}")
            user_attributes = [
                {"Name": "email", "Value": email},
                {"Name": "email_verified", "Value": "true"},
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

            logger.info(f"[EmployeeRegistration] Usuário criado com sucesso: {user.get('User', {}).get('Username')}")

            logger.info(f"[EmployeeRegistration] Iniciando autenticação ADMIN_USER_PASSWORD_AUTH para {email}")
            auth = self.cognito.admin_initiate_auth(
                user_pool_id=self.user_pool_id,
                client_id=self.app_client_id,
                auth_flow="ADMIN_USER_PASSWORD_AUTH",
                auth_parameters={"USERNAME": email, "PASSWORD": password}
            )

            challenge = auth.get("ChallengeName")
            logger.info(f"[EmployeeRegistration] Autenticação concluída com Challenge={challenge}")

            return response(201, {
                "message": "Usuário interno cadastrado com sucesso",
                "username": user["User"]["Username"],
                "challenge": challenge
            })

        except ClientError as e:
            logger.exception(f"[EmployeeRegistration] Erro Cognito ao criar usuário email={email}: {e}")
            return response(500, {"message": f"Erro Cognito: {e}"})

        except Exception as e:
            logger.exception(f"[EmployeeRegistration] Erro inesperado: {e}")
            return response(500, {"message": f"Erro interno: {e}"})
