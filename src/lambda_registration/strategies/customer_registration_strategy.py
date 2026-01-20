import os
import logging
from botocore.exceptions import ClientError
from ..utils.responses import response
from ..utils.cognito_client import CognitoClient

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class CustomerRegistrationStrategy:
    def __init__(self, cognito: CognitoClient = None):
        self.cognito = cognito or CognitoClient()
        self.user_pool_id = os.getenv("CUSTOMER_USER_POOL_ID")
        logger.info(f"[CustomerRegistrationStrategy] Inicializado com USER_POOL_ID={self.user_pool_id}")

    def execute(self, data):
        logger.info(f"[CustomerRegistration] Iniciando execução com dados: {data}")

        cpf = data.get("cpf")
        if not cpf:
            logger.warning("[CustomerRegistration] CPF não informado no payload.")
            return response(400, {"message": "Obrigatório enviar CPF"})

        try:
            logger.info(f"[CustomerRegistration] Verificando existência do usuário com CPF={cpf}")
            existing = self.cognito.get_user_by_username(self.user_pool_id, cpf)

            if existing:
                logger.info(f"[CustomerRegistration] Usuário com CPF={cpf} já cadastrado no Cognito.")
                return response(409, {"message": "Cliente já cadastrado"})

            logger.info(f"[CustomerRegistration] Criando novo usuário com CPF={cpf}")
            user = self.cognito.admin_create_user(
                user_pool_id=self.user_pool_id,
                username=cpf,
                user_attributes=[{"Name": "custom:cpf", "Value": cpf}],
                message_action="SUPPRESS"
            )

            user_id = user.get("User", {}).get("Username")
            logger.info(f"[CustomerRegistration] Usuário criado com sucesso: userId={user_id}")

            return response(201, {
                "message": "Cliente cadastrado com sucesso",
                "userId": user_id
            })

        except ClientError as e:
            logger.exception(f"[CustomerRegistration] Erro Cognito ao criar usuário CPF={cpf}: {e}")
            return response(500, {"message": f"Erro Cognito: {e}"})

        except Exception as e:
            logger.exception(f"[CustomerRegistration] Erro inesperado: {e}")
            return response(500, {"message": f"Erro interno: {e}"})
