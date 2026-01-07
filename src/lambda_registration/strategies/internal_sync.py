import os
import logging
from ..utils.db_client import DBClient
from ..utils.responses import response

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class InternalSyncStrategy:
    def __init__(self, db_client: DBClient = None):
        self.db = db_client or DBClient()
        self.table_name = os.getenv("INTERNAL_TABLE", "internal_users")

    def execute(self, data):
        logger.info(f"[InternalSync] Iniciando sincronizacao com dados: {data}")

        user_id = data.get("userId")
        email = data.get("email")
        name = data.get("name")

        if not user_id or not email:
            logger.warning("[InternalSync] userId e email são obrigatórios para sincronização")
            return response(400, {"message": "userId e email são obrigatórios para sincronização"})

        query = (
            f"INSERT INTO {self.table_name} (cognito_user_id, email, name) "
            "VALUES (%s, %s, %s) "
            "ON CONFLICT DO NOTHING"
        )

        try:
            self.db.execute(query, (user_id, email, name))
            logger.info("[InternalSync] Sincronizacao concluida com sucesso")
            return response(200, {"message": "Interno sincronizado com sucesso"})
        except Exception as e:
            logger.exception(f"[InternalSync] Falha ao sincronizar: {e}")
            return response(500, {"message": "Erro ao sincronizar interno"})
