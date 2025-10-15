import os
import logging
from typing import Optional, Any, Dict
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DEFAULT_REGION = "us-east-1"


class CognitoClient:
    """
    Wrapper em torno do boto3 Cognito IDP.
    Centraliza as chamadas, padroniza tratamento de erros e facilita os testes.
    """

    def __init__(self, client: Optional[Any] = None, region: Optional[str] = None):
        region = region or os.getenv("REGION") or os.getenv("AWS_REGION") or DEFAULT_REGION
        if client:
            self._client = client
        else:
            self._client = boto3.client("cognito-idp", region_name=region)

    def list_users(self, user_pool_id: str, filter_str: str, limit: int = 60) -> Dict:
        """Lista usuários do user pool com filtro."""
        try:
            return self._client.list_users(UserPoolId=user_pool_id, Filter=filter_str, Limit=limit)
        except ClientError as e:
            logger.exception("Erro ao listar usuários do Cognito")
            raise

    def admin_create_user(
        self,
        user_pool_id: str,
        username: str,
        user_attributes: list,
        temporary_password: Optional[str] = None,
        message_action: Optional[str] = None,
    ) -> Dict:
        """Cria usuário no Cognito via admin_create_user."""
        kwargs = {
            "UserPoolId": user_pool_id,
            "Username": username,
            "UserAttributes": [attr for attr in user_attributes if attr],
        }

        if temporary_password:
            kwargs["TemporaryPassword"] = temporary_password
        if message_action:
            kwargs["MessageAction"] = message_action

        try:
            return self._client.admin_create_user(**kwargs)
        except ClientError as e:
            logger.exception("Erro ao criar usuário no Cognito")
            raise

    def admin_initiate_auth(
        self,
        user_pool_id: str,
        client_id: str,
        auth_flow: str,
        auth_parameters: dict,
    ) -> Dict:
        """Inicia autenticação administrativa."""
        try:
            return self._client.admin_initiate_auth(
                UserPoolId=user_pool_id,
                ClientId=client_id,
                AuthFlow=auth_flow,
                AuthParameters=auth_parameters,
            )
        except ClientError as e:
            logger.warning("Erro ao iniciar auth admin, tentando fallback...")
            try:
                return self._client.admin_initiate_auth(
                    ClientId=client_id,
                    AuthFlow=auth_flow,
                    AuthParameters=auth_parameters,
                )
            except ClientError:
                logger.exception("Erro definitivo ao iniciar auth admin no Cognito")
                raise

    def get_user_by_username(self, user_pool_id: str, username: str) -> Optional[Dict]:
        """Retorna um usuário pelo username, se existir."""
        filter_str = f'username = "{username}"'
        try:
            res = self.list_users(user_pool_id=user_pool_id, filter_str=filter_str, limit=1)
            users = res.get("Users") or []
            return users[0] if users else None
        except ClientError:
            raise
