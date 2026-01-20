import json
import os
import boto3
import jwt
from datetime import datetime, timedelta, timezone
from botocore.exceptions import ClientError

# --- Variáveis de Ambiente ---
USER_POOLS = os.environ.get("USER_POOLS", "customer:us-east-1_R7bhXa09B")  
JWT_SECRET = os.environ.get("JWT_SECRET", "TESTE_SECRET")  
REGION = os.environ.get("REGION", "us-east-1")

# Converte em dict { "customer": "id" }
POOL_MAP = dict(item.split(":") for item in USER_POOLS.split(",") if ":" in item)
cognito_client = boto3.client("cognito-idp", region_name=REGION)

def handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
    except json.JSONDecodeError:
        return _response(400, {"message": "Corpo inválido: precisa ser JSON"})

    cpf = body.get("cpf")
    if not cpf:
        return _response(400, {"message": "Obrigatório enviar CPF"})

    try:
        user_pool_id = POOL_MAP.get("customer")
        if not user_pool_id:
            return _response(500, {"message": "User pool de customer não configurada"})

        response = cognito_client.list_users(
            UserPoolId=user_pool_id,
            Filter=f'username = "{cpf}"',
            Limit=1
        )

        users = response.get("Users", [])
        if not users:
            return _response(404, {"message": "Cliente não encontrado"})

        user = users[0]
        payload = {
            "sub": user["Username"],
            "role": "ROLE_CUSTOMER",
            "userPoolId": user_pool_id,
            "iat": int(datetime.now(timezone.utc).timestamp()),
            "exp": int((datetime.now(timezone.utc) + timedelta(hours=1)).timestamp())
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

        return _response(200, {
            "message": "Autenticação por CPF bem-sucedida",
            "token": token,
            "role": "ROLE_CUSTOMER",
            "userId": user["Username"]
        })

    except ClientError as e:
        return _response(500, {"message": f"Erro Cognito: {e}"})
    except Exception as e:
        return _response(500, {"message": "Erro interno do servidor"})

def _response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(body)
    }
