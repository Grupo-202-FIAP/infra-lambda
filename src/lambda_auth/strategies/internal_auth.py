import os
import boto3
from botocore.exceptions import ClientError
from utils.responses import response

REGION = os.environ.get("REGION", "us-east-1")
INTERNAL_APP_CLIENT_ID = os.environ.get("INTERNAL_APP_CLIENT_ID")
USER_POOLS = os.environ.get("USER_POOLS", "internal:us-east-1_UNnANkTz9")
POOL_MAP = dict(item.split(":") for item in USER_POOLS.split(",") if ":" in item)

cognito_client = boto3.client("cognito-idp", region_name=REGION)

class InternalAuthStrategy:
    def authenticate(self, body):
        email = body.get("email")
        password = body.get("password")
        new_password = body.get("new_password")

        if not email or not password:
            return response(400, {"message": "Obrigatório enviar email e senha"})

        user_pool_id = POOL_MAP.get("internal")
        if not user_pool_id:
            return response(500, {"message": "User pool de internal não configurada"})

        try:
            resp = cognito_client.admin_initiate_auth(
                UserPoolId=user_pool_id,
                ClientId=INTERNAL_APP_CLIENT_ID,
                AuthFlow="ADMIN_USER_PASSWORD_AUTH",
                AuthParameters={"USERNAME": email, "PASSWORD": password}
            )

            if resp.get("ChallengeName") == "NEW_PASSWORD_REQUIRED":
                if not new_password:
                    return response(403, {
                        "message": "Usuário precisa trocar a senha",
                        "challenge": "NEW_PASSWORD_REQUIRED",
                        "session": resp.get("Session")
                    })
                resp = cognito_client.admin_respond_to_auth_challenge(
                    UserPoolId=user_pool_id,
                    ClientId=INTERNAL_APP_CLIENT_ID,
                    ChallengeName="NEW_PASSWORD_REQUIRED",
                    ChallengeResponses={"USERNAME": email, "NEW_PASSWORD": new_password},
                    Session=resp["Session"]
                )

            auth_result = resp.get("AuthenticationResult")
            if not auth_result:
                return response(401, {"message": "Falha na autenticação"})

            return response(200, {
                "message": "Login interno bem-sucedido",
                "idToken": auth_result.get("IdToken"),
                "accessToken": auth_result.get("AccessToken"),
                "refreshToken": auth_result.get("RefreshToken"),
                "role": "ROLE_EMPLOYEE"
            })

        except ClientError as e:
            return response(500, {"message": f"Erro Cognito: {e}"})
