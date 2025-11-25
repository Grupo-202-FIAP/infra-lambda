import os
import boto3
import logging
from botocore.exceptions import ClientError
from ..utils.responses import response

logger = logging.getLogger()
logger.setLevel(logging.INFO)

REGION = os.environ.get("REGION", "us-east-1")
INTERNAL_APP_CLIENT_ID = os.environ.get("INTERNAL_APP_CLIENT_ID")
INTERNAL_USER_POOL = os.environ.get("INTERNAL_USER_POOL_ID")

cognito_client = boto3.client("cognito-idp", region_name=REGION)


class InternalRegistrationStrategy:

    def execute(self, data):
        logger.info(f"[InternalRegistration] Iniciando execução com dados: {data}")

        email = data.get("email")
        password = data.get("password")
        name = data.get("name")

        if not email or not password:
            logger.warning("[InternalRegistration] Campos obrigatórios ausentes: email e/ou password.")
            return response(400, {"message": "Obrigatório enviar email e password"})

        try:
            logger.info(f"[InternalRegistration] Criando usuário interno com email={email}")
            user_attributes = [ 
                {"Name": "email", "Value": email},
                {"Name": "email_verified", "Value": "true"},
            ]
            if name:
                user_attributes.append({"Name": "name", "Value": name})

            user = cognito_client.admin_create_user(
                UserPoolId=INTERNAL_USER_POOL,
                Username=email,
                UserAttributes=user_attributes,
                TemporaryPassword=password,
                MessageAction="SUPPRESS"
            )

            logger.info(f"[InternalRegistration] Usuário criado com sucesso: {user.get('User', {}).get('Username')}")

            logger.info(f"[InternalRegistration] Iniciando autenticação ADMIN_USER_PASSWORD_AUTH para {email}")
            auth = cognito_client.admin_initiate_auth(
                UserPoolId=INTERNAL_USER_POOL,
                ClientId=INTERNAL_APP_CLIENT_ID,
                AuthFlow="ADMIN_USER_PASSWORD_AUTH",
                AuthParameters={"USERNAME": email, "PASSWORD": password}
            )

            challenge = auth.get("ChallengeName")
            logger.info(f"[InternalRegistration] Autenticação concluída com Challenge={challenge}")

            return response(201, {
                "message": "Usuário interno cadastrado com sucesso",
                "username": user["User"]["Username"],
                "challenge": challenge
            })

        except ClientError as e:
            logger.exception(f"[InternalRegistration] Erro Cognito ao criar usuário email={email}: {e}")
            return response(500, {"message": f"Erro Cognito: {e}"})

        except Exception as e:
            logger.exception(f"[InternalRegistration] Erro inesperado: {e}")
            return response(500, {"message": f"Erro interno: {e}"})
