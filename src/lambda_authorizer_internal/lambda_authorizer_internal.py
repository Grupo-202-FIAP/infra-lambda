import json
import os
import boto3
from botocore.exceptions import ClientError

# --- Variáveis de Ambiente ---
USER_POOLS = os.environ.get("USER_POOLS", "internal:us-east-1_UNnANkTz9")  
REGION = os.environ.get("REGION", "us-east-1")
INTERNAL_APP_CLIENT_ID = os.environ.get("INTERNAL_APP_CLIENT_ID")  

# Converte em dict { "internal": "id" }
POOL_MAP = dict(item.split(":") for item in USER_POOLS.split(",") if ":" in item)
cognito_client = boto3.client("cognito-idp", region_name=REGION)

def handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
    except json.JSONDecodeError:
        return _response(400, {"message": "Corpo inválido: precisa ser JSON"})

    email = body.get("email")
    password = body.get("password")
    new_password = body.get("new_password")

    if not email or not password:
        return _response(400, {"message": "Obrigatório enviar email e senha"})

    try:
        user_pool_id = POOL_MAP.get("internal")
        if not user_pool_id:
            return _response(500, {"message": "User pool de internal não configurada"})
        if not INTERNAL_APP_CLIENT_ID:
            return _response(500, {"message": "App Client ID interno não configurado"})

        response = cognito_client.admin_initiate_auth(
            UserPoolId=user_pool_id,
            ClientId=INTERNAL_APP_CLIENT_ID,
            AuthFlow="ADMIN_USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": email,
                "PASSWORD": password
            }
        )

        # NEW_PASSWORD_REQUIRED challenge
        if response.get("ChallengeName") == "NEW_PASSWORD_REQUIRED":
            if not new_password:
                return _response(403, {
                    "message": "Usuário precisa trocar a senha",
                    "challenge": "NEW_PASSWORD_REQUIRED",
                    "session": response.get("Session")
                })
            challenge_resp = cognito_client.admin_respond_to_auth_challenge(
                UserPoolId=user_pool_id,
                ClientId=INTERNAL_APP_CLIENT_ID,
                ChallengeName="NEW_PASSWORD_REQUIRED",
                ChallengeResponses={
                    "USERNAME": email,
                    "NEW_PASSWORD": new_password
                },
                Session=response["Session"]
            )
            auth_result = challenge_resp.get("AuthenticationResult")
        else:
            auth_result = response.get("AuthenticationResult")

        if not auth_result:
            return _response(401, {"message": "Falha na autenticação"})

        return _response(200, {
            "message": "Login por email bem-sucedido",
            "idToken": auth_result.get("IdToken"),
            "accessToken": auth_result.get("AccessToken"),
            "refreshToken": auth_result.get("RefreshToken"),
            "role": "ROLE_EMPLOYEE"
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
