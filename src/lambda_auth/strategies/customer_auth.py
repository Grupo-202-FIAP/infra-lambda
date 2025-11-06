import os
import boto3
import jwt
from datetime import datetime, timedelta, timezone
from botocore.exceptions import ClientError
from ..utils.responses import response

REGION = os.environ.get("REGION", "us-east-1")
CUSTOMER_USER_POOL = os.environ.get("CUSTOMER_USER_POOL", "us-east-1_R7bhXa09B")
JWT_SECRET = os.environ.get("JWT_SECRET", "TESTE_SECRET")

cognito_client = boto3.client("cognito-idp", region_name=REGION)

class CustomerAuthStrategy:
    def authenticate(self, body):
        cpf = body.get("cpf")
        if not cpf:
            return response(400, {"message": "Obrigatório enviar CPF"})

        try:
            users = cognito_client.list_users(
                UserPoolId=CUSTOMER_USER_POOL,
                Filter=f'username = "{cpf}"',
                Limit=1
            ).get("Users", [])

            if not users:
                return response(404, {"message": "Cliente não encontrado"})

            user = users[0]
            payload = {
                "sub": user["Username"],
                "role": "ROLE_CUSTOMER",
                "userPoolId": CUSTOMER_USER_POOL,
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
