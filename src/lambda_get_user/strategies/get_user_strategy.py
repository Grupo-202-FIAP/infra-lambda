import os
import logging
from lambda_get_user.strategies.base import BaseStrategy
from lambda_get_user.utils.db_client import DBClient
from lambda_get_user.utils.responses import response

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class GetUserStrategy(BaseStrategy):
    def __init__(self, db_client: DBClient = None):
        self.db = db_client or DBClient()
        self.customer_table = os.getenv("CUSTOMER_TABLE", "customers")
        self.internal_table = os.getenv("INTERNAL_TABLE", "internal_users")

    def execute(self, data):
        logger.info(f"[GetUserStrategy] Iniciando busca de usuário com dados: {data}")

        user_id = data.get("user_id") or data.get("id") or data.get("customer_id")
        email = data.get("email")
        cpf = data.get("cpf")

        if not any([user_id, email, cpf]):
            logger.warning("[GetUserStrategy] Nenhum parâmetro de busca fornecido")
            return response(400, {
                "message": "É necessário fornecer pelo menos um parâmetro de busca: user_id/id/customer_id, email ou cpf"
            })

        try:
            # Se houver CPF, buscamos somente em customers
            if cpf:
                where = []
                params = []
                where.append("cpf = %s")
                params.append(cpf)
                if user_id:
                    where.append("id = %s::uuid")
                    params.append(user_id)
                if email:
                    where.append("email = %s")
                    params.append(email)
                query = f"SELECT *, 'customer' AS type FROM {self.customer_table} WHERE " + " AND ".join(where) + " LIMIT 1"
                logger.info(f"[GetUserStrategy] Executando query customers por CPF")
                user = self.db.fetch_one(query, tuple(params))
                return self._respond_user(user)

            # Primeiro tenta em customers
            cust_where = []
            cust_params = []
            if user_id:
                cust_where.append("id = %s::uuid")
                cust_params.append(user_id)
            if email:
                cust_where.append("email = %s")
                cust_params.append(email)

            user = None
            if cust_where:
                query = f"SELECT *, 'customer' AS type FROM {self.customer_table} WHERE " + " AND ".join(cust_where) + " LIMIT 1"
                logger.info(f"[GetUserStrategy] Executando query customers")
                user = self.db.fetch_one(query, tuple(cust_params))

            # Se não achou, tenta internal
            if not user:
                int_where = []
                int_params = []
                if user_id:
                    int_where.append("id = %s::uuid")
                    int_params.append(user_id)
                if email:
                    int_where.append("email = %s")
                    int_params.append(email)

                if int_where:
                    query = f"SELECT *, 'internal' AS type FROM {self.internal_table} WHERE " + " AND ".join(int_where) + " LIMIT 1"
                    logger.info(f"[GetUserStrategy] Executando query internal_users")
                    user = self.db.fetch_one(query, tuple(int_params))

            return self._respond_user(user)

        except Exception as e:
            logger.exception(f"[GetUserStrategy] Erro ao buscar usuário: {e}")
            return response(500, {
                "message": "Erro interno ao buscar usuário"
            })

    def _respond_user(self, user):
        if not user:
            logger.info("[GetUserStrategy] Usuário não encontrado")
            return response(404, {"message": "Usuário não encontrado"})

        if 'password' in user:
            del user['password']

        # Garantir chave 'type'
        user_type = user.get('type') or ('cpf' in user and 'customer' or 'internal')
        user['type'] = user_type

        logger.info(f"[GetUserStrategy] Usuário encontrado: {user.get('email')} ({user_type})")
        return response(200, {
            "message": "Usuário encontrado com sucesso",
            "user": user
        })
import os
import logging
from lambda_get_user.strategies.base import BaseStrategy
from lambda_get_user.utils.db_client import DBClient
from lambda_get_user.utils.responses import response

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class GetUserStrategy(BaseStrategy):
    def __init__(self, db_client: DBClient = None):
        self.db = db_client or DBClient()
        self.customer_table = os.getenv("CUSTOMER_TABLE", "customers")
        self.internal_table = os.getenv("INTERNAL_TABLE", "internal_users")

    def execute(self, data):
        logger.info(f"[GetUserStrategy] Iniciando busca de usuário com dados: {data}")

        # Normalizar chaves de entrada (compatibilidade)
        user_id = data.get("user_id") or data.get("id") or data.get("customer_id")
        email = data.get("email")
        cpf = data.get("cpf")

        if not any([user_id, email, cpf]):
            logger.warning("[GetUserStrategy] Nenhum parâmetro de busca fornecido")
            return response(400, {
                "message": "É necessário fornecer pelo menos um parâmetro de busca: user_id/id/customer_id, email ou cpf"
            })

        try:
            # 1) Se CPF foi informado, só existe em customers
            if cpf:
                query_conditions = ["cpf = %s"]
                query_params = [cpf]
                if user_id:
                    query_conditions.append("id = %s::uuid")
                    query_params.append(user_id)
                if email:
                    query_conditions.append("email = %s")
                    query_params.append(email)

                where_clause = " AND ".join(query_conditions)
                query = f"SELECT * FROM {self.customer_table} WHERE {where_clause} LIMIT 1"
                logger.info(f"[GetUserStrategy] Executando query (customers por cpf): {query}")
                rec = self.db.fetch_one(query, tuple(query_params))
                if rec:
                    if 'password' in rec:
                        del rec['password']
                    rec['type'] = 'customer'
                    return response(200, {
                        "message": "Usuário encontrado com sucesso",
                        "user": rec
                    })

                logger.info("[GetUserStrategy] Usuário não encontrado (customers por cpf)")
                return response(404, {"message": "Usuário não encontrado"})

            # 2) Buscar por ID/Email em customers primeiro
            cust = None
            if user_id or email:
                query_conditions = []
                query_params = []
                if user_id:
                    query_conditions.append("id = %s::uuid")
                    query_params.append(user_id)
                if email:
                    query_conditions.append("email = %s")
                    query_params.append(email)
                if query_conditions:
                    where_clause = " AND ".join(query_conditions)
                    query = f"SELECT * FROM {self.customer_table} WHERE {where_clause} LIMIT 1"
                    logger.info(f"[GetUserStrategy] Executando query (customers): {query}")
                    cust = self.db.fetch_one(query, tuple(query_params))
                    if cust:
                        if 'password' in cust:
                            del cust['password']
                        cust['type'] = 'customer'
                        return response(200, {
                            "message": "Usuário encontrado com sucesso",
                            "user": cust
                        })

            # 3) Não encontrado em customers, tentar internal_users
            if user_id or email:
                query_conditions = []
                query_params = []
                if user_id:
                    query_conditions.append("id = %s::uuid")
                    query_params.append(user_id)
                if email:
                    query_conditions.append("email = %s")
                    query_params.append(email)
                where_clause = " AND ".join(query_conditions)
                query = f"SELECT * FROM {self.internal_table} WHERE {where_clause} LIMIT 1"
                logger.info(f"[GetUserStrategy] Executando query (internal): {query}")
                rec = self.db.fetch_one(query, tuple(query_params))
                if rec:
                    if 'password' in rec:
                        del rec['password']
                    rec['cpf'] = rec.get('cpf')  # pode não existir; manter None
                    rec['status'] = rec.get('status')  # pode não existir
                    rec['type'] = 'internal'
                    return response(200, {
                        "message": "Usuário encontrado com sucesso",
                        "user": rec
                    })

            logger.info("[GetUserStrategy] Usuário não encontrado em nenhuma tabela")
            return response(404, {"message": "Usuário não encontrado"})

        except Exception as e:
            logger.exception(f"[GetUserStrategy] Erro ao buscar usuário: {e}")
            return response(500, {"message": "Erro interno ao buscar usuário"})
