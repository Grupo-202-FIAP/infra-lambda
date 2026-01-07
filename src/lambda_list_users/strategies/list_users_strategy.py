import os
import logging
from lambda_list_users.strategies.base import BaseStrategy
from lambda_list_users.utils.db_client import DBClient
from lambda_list_users.utils.responses import response

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ListUsersStrategy(BaseStrategy):
    def __init__(self, db_client: DBClient = None):
        self.db = db_client or DBClient()
        self.customer_table = os.getenv("CUSTOMER_TABLE", "customers")
        self.internal_table = os.getenv("INTERNAL_TABLE", "internal_users")

    def execute(self, data):
        logger.info(f"[ListUsersStrategy] Iniciando listagem de usuários com dados: {data}")
        try:
            page = int(data.get("page", 1))
            per_page = int(data.get("per_page", 20))
            if page < 1:
                page = 1
            if per_page < 1 or per_page > 100:
                per_page = 20
        except (ValueError, TypeError):
            logger.warning("[ListUsersStrategy] Parâmetros de paginação inválidos")
            return response(400, {"message": "Parâmetros de paginação inválidos. 'page' e 'per_page' devem ser números inteiros"})

        status = data.get("status")
        email_filter = data.get("email")

        try:
            # Construir subqueries normalizadas
            cust_filters = []
            cust_params = []
            if status:
                cust_filters.append("status = %s")
                cust_params.append(status)
            if email_filter:
                cust_filters.append("email ILIKE %s")
                cust_params.append(f"%{email_filter}%")
            cust_where = f"WHERE {' AND '.join(cust_filters)}" if cust_filters else ""

            int_filters = []
            int_params = []
            if email_filter:
                int_filters.append("email ILIKE %s")
                int_params.append(f"%{email_filter}%")
            int_where = f"WHERE {' AND '.join(int_filters)}" if int_filters else ""

            union_sql = f"""
                (
                    SELECT 
                        'customer' AS type,
                        id,
                        cognito_user_id,
                        cpf,
                        email,
                        name,
                        status,
                        created_at,
                        updated_at
                    FROM {self.customer_table}
                    {cust_where}
                )
                UNION ALL
                (
                    SELECT 
                        'internal' AS type,
                        id,
                        cognito_user_id,
                        NULL::text AS cpf,
                        email,
                        name,
                        NULL::text AS status,
                        created_at,
                        updated_at
                    FROM {self.internal_table}
                    {int_where}
                )
            """

            # Count total
            count_query = f"SELECT COUNT(*) AS total FROM {union_sql} AS users"
            count_params = tuple(cust_params + int_params) if (cust_params or int_params) else None
            logger.info(f"[ListUsersStrategy] Executando query de contagem unificada | params={count_params}")
            count_result = self.db.fetch_one(count_query, count_params)
            total_records = count_result.get("total", 0) if count_result else 0

            # Pagination
            offset = (page - 1) * per_page
            list_query = f"""
                SELECT * FROM {union_sql} AS users
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
            """
            list_params = list(cust_params + int_params)
            list_params.extend([per_page, offset])

            logger.info(f"[ListUsersStrategy] Executando query de listagem unificada | params={tuple(list_params)}")
            users = self.db.fetch_all(list_query, tuple(list_params) if list_params else (per_page, offset))

            for user in users:
                if 'password' in user:
                    del user['password']

            total_pages = (total_records + per_page - 1) // per_page if total_records > 0 else 0
            has_next = page < total_pages
            has_previous = page > 1

            logger.info(f"[ListUsersStrategy] Encontrados {len(users)} usuários de {total_records} total")

            return response(200, {
                "message": "Usuários listados com sucesso",
                "users": users,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total_records": total_records,
                    "total_pages": total_pages,
                    "has_next": has_next,
                    "has_previous": has_previous
                }
            })
        except Exception as e:
            logger.exception(f"[ListUsersStrategy] Erro ao listar usuários: {e}")
            return response(500, {"message": f"Erro interno ao listar usuários: {str(e)}"})
