import json
import os
import boto3
from botocore.exceptions import ClientError

REGION = os.environ.get("REGION", "us-east-1")
USER_POOL_ID = os.environ.get("USER_POOL_ID")

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
        # Verifica se usuário já existe
        existing = cognito_client.list_users(
            UserPoolId=USER_POOL_ID,
            Filter=f'username = "{cpf}"',
            Limit=1
        )
        if existing.get("Users"):
            return _response(409, {"message": "Cliente já cadastrado"})

        # Cria usuário
        response = cognito_client.admin_create_user(
            UserPoolId=USER_POOL_ID,
            Username=cpf,
            UserAttributes=[
                {"Name": "custom:cpf", "Value": cpf}
            ],
            MessageAction="SUPPRESS"
        )

        return _response(201, {
            "message": "Cliente cadastrado com sucesso",
            "userId": response["User"]["Username"]
        })

    except ClientError as e:
        print(f"Erro Cognito: {e}")
        return _response(500, {"message": f"Erro Cognito: {e}"})
    except Exception as e:
        print(f"Erro interno: {e}")
        return _response(500, {"message": "Erro interno do servidor"})


def _response(status, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        "body": json.dumps(body)
    }
