import json
import os
from .base import BaseStrategy
from ..utils.db_client import DBClient
from ..utils.responses import response


class CustomerSyncStrategy(BaseStrategy):
    def __init__(self):
        self.db = DBClient()

    def execute(self, data: dict) -> dict:
        user_id = data.get("userId")
        cpf = data.get("cpf")
        email = data.get("email")
        name = data.get("name")

        if not user_id:
            return response(400, {"message": "userId obrigatório para sync"})

        try:
            sql = """
                INSERT INTO customers (id_cognito, cpf, nome, email)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id_cognito) DO UPDATE
                SET cpf = EXCLUDED.cpf, nome = EXCLUDED.nome, email = EXCLUDED.email;
            """
            params = (user_id, cpf, name, email)
            self.db.execute(sql, params)
            return response(200, {"message": "Customer sincronizado"})
        except Exception as e:
            return response(500, {"message": f"Erro ao sincronizar customer: {str(e)}"})