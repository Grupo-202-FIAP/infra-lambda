import os
import boto3
import jwt
from datetime import datetime, timedelta, timezone
from botocore.exceptions import ClientError
from utils.responses import response

REGION = os.environ.get("REGION", "us-east-1")
USER_POOLS = os.environ.get("USER_POOLS", "customer:us-east-1_R7bhXa09B")
JWT_SECRET = os.environ.get("JWT_SECRET", "TESTE_SECRET")

POOL_MAP = dict(item.split(":") for item in USER_POOLS.split(",") if ":" in item)
cognito_client = boto3.client("cognito-idp", region_name=REGION)

class CustomerAuthStrategy:
    def authenticate(self, body):
        cpf = body.get("cpf")
        if not cpf:
            return response(400, {"message": "Obrigatório enviar CPF"})

        user_pool_id = POOL_MAP.get("customer")
        if not user_pool_id:
            return response(500, {"message": "User pool de customer não configurada"})

        try:
            users = cognito_client.list_users(
                UserPoolId=user_pool_id,
                Filter=f'username = "{cpf}"',
                Limit=1
            ).get("Users", [])

            if not users:
                return response(404, {"message": "Cliente não encontrado"})

            user = users[0]
            payload = {
                "sub": user["Username"],
                "role": "ROLE_CUSTOMER",
                "userPoolId": user_pool_id,
                "iat": int(datetime.now(timezone.utc).timestamp()),
                "exp": int((datetime.now(timezone.utc) + timedelta(hours=1)).timestamp())
            }

            token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

            return response(200, {
                "message": "Autenticação por CPF bem-sucedida",
                "token": token,
                "role": "ROLE_CUSTOMER",
                "userId": user["Username"]
            })

        except ClientError as e:
            return response(500, {"message": f"Erro Cognito: {e}"})
