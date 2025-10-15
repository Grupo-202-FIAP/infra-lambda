import os
from botocore.exceptions import ClientError
from ..utils.responses import response
from ..utils.cognito_client import CognitoClient


class CustomerRegistrationStrategy:
    def __init__(self, cognito: CognitoClient = None):
        self.cognito = cognito or CognitoClient()
        self.user_pool_id = os.getenv("CUSTOMER_USER_POOL_ID")

    def execute(self, data):
        cpf = data.get("cpf")
        if not cpf:
            return response(400, {"message": "Obrigatório enviar CPF"})

        try:
            existing = self.cognito.get_user_by_username(self.user_pool_id, cpf)
            if existing:
                return response(409, {"message": "Cliente já cadastrado"})

            user = self.cognito.admin_create_user(
                user_pool_id=self.user_pool_id,
                username=cpf,
                user_attributes=[{"Name": "custom:cpf", "Value": cpf}],
                message_action="SUPPRESS"
            )

            return response(201, {
                "message": "Cliente cadastrado com sucesso",
                "userId": user["User"]["Username"]
            })
        except ClientError as e:
            return response(500, {"message": f"Erro Cognito: {e}"})
