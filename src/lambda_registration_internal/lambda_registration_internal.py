import json
import os
import boto3
from botocore.exceptions import ClientError

REGION = os.environ.get("REGION", "us-east-1")
USER_POOL_ID = os.environ.get("USER_POOL_ID")
APP_CLIENT_ID = os.environ.get("INTERNAL_APP_CLIENT_ID")

cognito_client = boto3.client("cognito-idp", region_name=REGION)

def handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
    except json.JSONDecodeError:
        return _response(400, {"message": "Corpo inválido: precisa ser JSON"})

    email = body.get("email")
    password = body.get("password")
    name = body.get("name")

    if not email or not password:
        return _response(400, {"message": "Obrigatório enviar email e password"})

    try:
        response = cognito_client.admin_create_user(
            UserPoolId=USER_POOL_ID,
            Username=email,
            UserAttributes=[
                {"Name": "email", "Value": email},
                {"Name": "email_verified", "Value": "true"},
                {"Name": "name", "Value": name} if name else {}
            ],
            TemporaryPassword=password,
            MessageAction="SUPPRESS"
        )

        # Força troca imediata de senha
        challenge_resp = cognito_client.admin_initiate_auth(
            UserPoolId=USER_POOL_ID,
            ClientId=APP_CLIENT_ID,
            AuthFlow="ADMIN_USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": email,
                "PASSWORD": password
            }
        )

        return _response(201, {
            "message": "Usuário interno cadastrado com sucesso",
            "username": response["User"]["Username"],
            "challenge": challenge_resp.get("ChallengeName")
        })

    except ClientError as e:
        print(f"Erro Cognito: {e}")
        return _response(500, {"message": f"Erro Cognito: {e}"})
    except Exception as e:
        print(f"Erro interno: {e}")
        return _response(500, {"message": "Erro interno do servidor:"})


def _response(status, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        "body": json.dumps(body)
    }
