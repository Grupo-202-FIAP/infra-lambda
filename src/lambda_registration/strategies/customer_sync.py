import json
import logging
from .base import BaseStrategy
from ..utils.db_client import DBClient
from ..utils.responses import response

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class CustomerSyncStrategy(BaseStrategy):
    def __init__(self):
        self.db = DBClient()
        logger.info("[CustomerSyncStrategy] Inicializado DBClient para sync de customers")

    def execute(self, data: dict) -> dict:
        logger.info(f"[CustomerSync] Dados recebidos para sync: {data}")

        user_id = data.get("userId")
        cpf = data.get("cpf")
        email = data.get("email")
        name = data.get("name")

        if not user_id:
            logger.warning("[CustomerSync] userId ausente no payload")
            return response(400, {"message": "userId obrigatório para sync"})

        try:
            sql = """
                INSERT INTO customers (id_cognito, cpf, nome, email)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id_cognito) DO UPDATE
                SET cpf = EXCLUDED.cpf, nome = EXCLUDED.nome, email = EXCLUDED.email;
            """
            params = (user_id, cpf, name, email)
            logger.info(f"[CustomerSync] Executando SQL: {sql.strip()} com params={params}")
            self.db.execute(sql, params)
            logger.info(f"[CustomerSync] Customer sincronizado com sucesso: userId={user_id}")
            return response(200, {"message": "Customer sincronizado"})

        except Exception as e:
            logger.exception(f"[CustomerSync] Erro ao sincronizar customer userId={user_id}: {e}")
            return response(500, {"message": f"Erro ao sincronizar customer: {str(e)}"})
