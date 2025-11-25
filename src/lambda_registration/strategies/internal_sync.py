import json
import logging
from .base import BaseStrategy
from ..utils.db_client import DBClient
from ..utils.responses import response

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class InternalSyncStrategy(BaseStrategy):
    def __init__(self):
        self.db = DBClient()
        logger.info("[InternalSyncStrategy] Inicializado DBClient para sync de internos")

    def execute(self, data: dict) -> dict:
        logger.info(f"[InternalSync] Dados recebidos para sync: {data}")

        user_id = data.get("userId")
        email = data.get("email")
        name = data.get("name")

        if not user_id or not email:
            logger.warning("[InternalSync] userId ou email ausente no payload")
            return response(400, {"message": "userId e email são obrigatórios para sync"})

        try:
            sql = """
                INSERT INTO usuarios (id_cognito, nome, email)
                VALUES (%s, %s, %s)
                ON CONFLICT (id_cognito) DO UPDATE
                SET nome = EXCLUDED.nome, email = EXCLUDED.email;
            """
            params = (user_id, name, email)
            logger.info(f"[InternalSync] Executando SQL: {sql.strip()} com params={params}")
            self.db.execute(sql, params)
            logger.info(f"[InternalSync] Interno sincronizado com sucesso: userId={user_id}")
            return response(200, {"message": "Interno sincronizado"})

        except Exception as e:
            logger.exception(f"[InternalSync] Erro ao sincronizar interno userId={user_id}: {e}")
            return response(500, {"message": f"Erro ao sincronizar interno: {str(e)}"})

