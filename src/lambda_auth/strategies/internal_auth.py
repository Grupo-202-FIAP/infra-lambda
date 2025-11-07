import os
import boto3
import logging
from botocore.exceptions import ClientError
from ..utils.responses import response

logger = logging.getLogger()
logger.setLevel(logging.INFO)

REGION = os.environ.get("REGION", "us-east-1")
INTERNAL_APP_CLIENT_ID = os.environ.get("INTERNAL_APP_CLIENT_ID")
INTERNAL_USER_POOL = os.environ.get("INTERNAL_USER_POOL", "us-east-1_UNnANkTz9")

cognito_client = boto3.client("cognito-idp", region_name=REGION)

class InternalAuthStrategy:
    def authenticate(self, body):
        logger.info("==== Iniciando autenticação do tipo 'internal' ====")
        logger.info(f"Body recebido: {body}")

        email = body.get("email")
        password = body.get("password")
        new_password = body.get("new_password")

        if not email or not password:
            logger.warning("Campos obrigatórios 'email' e/ou 'password' ausentes.")
            return response(400, {"message": "Obrigatório enviar email e senha"})

        try:
            logger.info(f"Iniciando fluxo ADMIN_USER_PASSWORD_AUTH no Cognito para o usuário: {email}")
            resp = cognito_client.admin_initiate_auth(
                UserPoolId=INTERNAL_USER_POOL,
                ClientId=INTERNAL_APP_CLIENT_ID,
                AuthFlow="ADMIN_USER_PASSWORD_AUTH",
                AuthParameters={"USERNAME": email, "PASSWORD": password}
            )
            logger.info(f"Resposta inicial do Cognito: {resp}")

            # Caso o usuário precise trocar a senha
            if resp.get("ChallengeName") == "NEW_PASSWORD_REQUIRED":
                logger.info(f"Usuário {email} possui desafio NEW_PASSWORD_REQUIRED")

                if not new_password:
                    logger.warning("Usuário precisa trocar a senha, mas 'new_password' não foi informado.")
                    return response(403, {
                        "message": "Usuário precisa trocar a senha",
                        "challenge": "NEW_PASSWORD_REQUIRED",
                        "session": resp.get("Session")
                    })

                logger.info(f"Respondendo ao desafio NEW_PASSWORD_REQUIRED para o usuário {email}")
                resp = cognito_client.admin_respond_to_auth_challenge(
                    UserPoolId=INTERNAL_USER_POOL,
                    ClientId=INTERNAL_APP_CLIENT_ID,
                    ChallengeName="NEW_PASSWORD_REQUIRED",
                    ChallengeResponses={
                        "USERNAME": email,
                        "NEW_PASSWORD": new_password
                    },
                    Session=resp["Session"]
                )
                logger.info(f"Resposta do Cognito após troca de senha: {resp}")

            auth_result = resp.get("AuthenticationResult")
            if not auth_result:
                logger.error(f"Falha na autenticação para o usuário {email}. Resposta sem AuthenticationResult.")
                return response(401, {"message": "Falha na autenticação"})

            logger.info(f"Autenticação bem-sucedida para o usuário {email}")
            result = response(200, {
                "message": "Login interno bem-sucedido",
                "idToken": auth_result.get("IdToken"),
                "accessToken": auth_result.get("AccessToken"),
                "refreshToken": auth_result.get("RefreshToken"),
                "role": "ROLE_EMPLOYEE"
            })

            logger.info(f"Resposta final da autenticação interna: {result}")
            logger.info("==== Autenticação 'internal' concluída com sucesso ====")
            return result

        except ClientError as e:
            logger.exception(f"Erro de comunicação com o Cognito para o usuário {email}: {e}")
            return response(500, {"message": f"Erro Cognito: {e}"})

        except Exception as e:
            logger.exception(f"Erro inesperado durante autenticação interna: {e}")
            return response(500, {"message": f"Erro interno do servidor: {e}"})
