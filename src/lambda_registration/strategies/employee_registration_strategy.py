import os
from botocore.exceptions import ClientError
from ..utils.responses import response
from ..utils.cognito_client import CognitoClient


class EmployeeRegistrationStrategy:
    def __init__(self, cognito: CognitoClient = None):
        self.cognito = cognito or CognitoClient()
        self.user_pool_id = os.getenv("USER_POOL_ID")
        self.app_client_id = os.getenv("INTERNAL_APP_CLIENT_ID")

    def execute(self, data):
        email = data.get("email")
        password = data.get("password")
        name = data.get("name")

        if not email or not password:
            return response(400, {"message": "Obrigatório enviar email e password"})

        try:
            user = self.cognito.admin_create_user(
                user_pool_id=self.user_pool_id,
                username=email,
                user_attributes=[
                    {"Name": "email", "Value": email},
                    {"Name": "email_verified", "Value": "true"},
                    {"Name": "name", "Value": name} if name else None
                ],
                temporary_password=password,
                message_action="SUPPRESS"
            )

            auth = self.cognito.admin_initiate_auth(
                user_pool_id=self.user_pool_id,
                client_id=self.app_client_id,
                auth_flow="ADMIN_USER_PASSWORD_AUTH",
                auth_parameters={"USERNAME": email, "PASSWORD": password}
            )

            return response(201, {
                "message": "Usuário interno cadastrado com sucesso",
                "username": user["User"]["Username"],
                "challenge": auth.get("ChallengeName")
            })
        except ClientError as e:
            return response(500, {"message": f"Erro Cognito: {e}"})
