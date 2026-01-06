import os
import logging
from ..utils.db_client import DBClient
from ..utils.responses import response

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class CustomerSyncStrategy:
    def __init__(self, db_client: DBClient = None):
        self.db = db_client or DBClient()
        self.table_name = os.getenv("CUSTOMER_TABLE", "customers")

    def execute(self, data):
        logger.info(f"[CustomerSync] Iniciando sincronizacao com dados: {data}")

        user_id = data.get("userId")
        cpf = data.get("cpf")
        email = data.get("email")
        name = data.get("name")

        if not user_id:
            logger.warning("[CustomerSync] userId obrigatorio para sincronizacao")
            return response(400, {"message": "userId obrigatorio para sincronizacao"})

        query = (
            f"INSERT INTO {self.table_name} (cognito_user_id, cpf, email, name) "
            "VALUES (%s, %s, %s, %s) "
            "ON CONFLICT DO NOTHING"
        )

        try:
            self.db.execute(query, (user_id, cpf, email, name))
            logger.info("[CustomerSync] Sincronizacao concluida com sucesso")
            return response(200, {"message": "Customer sincronizado com sucesso"})
        except Exception as e:
            logger.exception(f"[CustomerSync] Falha ao sincronizar: {e}")
            return response(500, {"message": f"Erro ao sincronizar customer: {e}"})
