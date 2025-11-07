import os
import boto3
import jwt
import logging
from datetime import datetime, timedelta, timezone
from botocore.exceptions import ClientError
from ..utils.responses import response

logger = logging.getLogger()
logger.setLevel(logging.INFO)

REGION = os.environ.get("REGION", "us-east-1")
CUSTOMER_USER_POOL = os.environ.get("CUSTOMER_USER_POOL", "us-east-1_R7bhXa09B")
JWT_SECRET = os.environ.get("JWT_SECRET", "TESTE_SECRET")

cognito_client = boto3.client("cognito-idp", region_name=REGION)

class CustomerAuthStrategy:
    def authenticate(self, body):
        logger.info("==== Iniciando autenticação do tipo 'customer' ====")
        logger.info(f"Body recebido: {body}")

        cpf = body.get("cpf")
        if not cpf:
            logger.warning("Campo 'cpf' ausente no body.")
            return response(400, {"message": "Obrigatório enviar CPF"})

        try:
            logger.info(f"Consultando usuário no Cognito pelo CPF: {cpf}")
            users = cognito_client.list_users(
                UserPoolId=CUSTOMER_USER_POOL,
                Filter=f'username = "{cpf}"',
                Limit=1
            ).get("Users", [])

            logger.info(f"Resultado da busca no Cognito: {users}")

            if not users:
                logger.warning(f"Nenhum usuário encontrado para o CPF: {cpf}")
                return response(404, {"message": "Cliente não encontrado"})

            user = users[0]
            logger.info(f"Usuário encontrado: {user['Username']}")

            # Montagem do payload JWT
            payload = {
                "sub": user["Username"],
                "role": "ROLE_CUSTOMER",
                "userPoolId": CUSTOMER_USER_POOL,
                "iat": int(datetime.now(timezone.utc).timestamp()),
                "exp": int((datetime.now(timezone.utc) + timedelta(hours=1)).timestamp())
            }
            logger.info(f"Payload JWT gerado: {payload}")

            token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
            logger.info("Token JWT gerado com sucesso.")

            result = response(200, {
                "message": "Autenticação por CPF bem-sucedida",
                "token": token,
                "role": "ROLE_CUSTOMER",
                "userId": user["Username"]
            })

            logger.info(f"Resposta final da autenticação: {result}")
            logger.info("==== Autenticação 'customer' concluída com sucesso ====")
            return result

        except ClientError as e:
            logger.exception(f"Erro ao consultar o Cognito: {e}")
            return response(500, {"message": f"Erro Cognito: {e}"})

        except Exception as e:
            logger.exception(f"Erro inesperado durante autenticação: {e}")
            return response(500, {"message": f"Erro interno do servidor: {e}"})
