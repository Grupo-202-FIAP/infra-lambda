import json
from .base import BaseStrategy
from ..utils.db_client import DBClient
from ..utils.responses import response


class EmployeeSyncStrategy(BaseStrategy):
    def __init__(self):
        self.db = DBClient()

    def execute(self, data: dict) -> dict:
        user_id = data.get("userId")
        email = data.get("email")
        name = data.get("name")

        if not user_id or not email:
            return response(400, {"message": "userId e email são obrigatórios para sync"})

        try:
            sql = """
                INSERT INTO usuarios (id_cognito, nome, email)
                VALUES (%s, %s, %s)
                ON CONFLICT (id_cognito) DO UPDATE
                SET nome = EXCLUDED.nome, email = EXCLUDED.email;
            """
            params = (user_id, name, email)
            self.db.execute(sql, params)
            return response(200, {"message": "Employee sincronizado"})
        except Exception as e:
            return response(500, {"message": f"Erro ao sincronizar employee: {str(e)}"})