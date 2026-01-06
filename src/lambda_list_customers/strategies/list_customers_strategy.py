import os
import logging
from lambda_list_customers.strategies.base import BaseStrategy
from lambda_list_customers.utils.db_client import DBClient
from lambda_list_customers.utils.responses import response

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ListCustomersStrategy(BaseStrategy):
    def __init__(self, db_client: DBClient = None):
        self.db = db_client or DBClient()
        self.table_name = os.getenv("CUSTOMER_TABLE", "customers")

    def execute(self, data):
        logger.info(f"[ListCustomersStrategy] Iniciando listagem de clientes com dados: {data}")

        # Parâmetros de paginação
        try:
            page = int(data.get("page", 1))
            per_page = int(data.get("per_page", 20))
            
            if page < 1:
                page = 1
            if per_page < 1 or per_page > 100:
                per_page = 20
                
        except (ValueError, TypeError):
            logger.warning("[ListCustomersStrategy] Parâmetros de paginação inválidos")
            return response(400, {
                "message": "Parâmetros de paginação inválidos. 'page' e 'per_page' devem ser números inteiros"
            })

        # Parâmetros de filtro opcionais
        status = data.get("status")
        email_filter = data.get("email")

        # Construir query com filtros
        query_conditions = []
        query_params = []
        count_params = []

        # Filtro por status (se existir a coluna)
        if status:
            query_conditions.append("status = %s")
            query_params.append(status)
            count_params.append(status)

        # Filtro por email (busca parcial com LIKE)
        if email_filter:
            query_conditions.append("email ILIKE %s")
            query_params.append(f"%{email_filter}%")
            count_params.append(f"%{email_filter}%")

        # Montar WHERE clause
        where_clause = ""
        if query_conditions:
            where_clause = "WHERE " + " AND ".join(query_conditions)

        # Calcular offset
        offset = (page - 1) * per_page

        try:
            # Query para contar total de registros
            count_query = f"SELECT COUNT(*) as total FROM {self.table_name} {where_clause}"
            logger.info(f"[ListCustomersStrategy] Executando query de contagem: {count_query}")
            
            count_result = self.db.fetch_one(count_query, tuple(count_params) if count_params else None)
            total_records = count_result.get("total", 0) if count_result else 0

            # Query para buscar registros com paginação
            query = f"""
                SELECT 
                    id,
                    cognito_user_id,
                    cpf,
                    email,
                    name,
                    status,
                    created_at,
                    updated_at
                FROM {self.table_name}
                {where_clause}
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
            """
            
            # Adicionar limit e offset aos parâmetros
            query_params.extend([per_page, offset])
            
            logger.info(f"[ListCustomersStrategy] Executando query de listagem: {query}")
            customers = self.db.fetch_all(query, tuple(query_params))

            # Calcular metadados de paginação
            total_pages = (total_records + per_page - 1) // per_page if total_records > 0 else 0
            has_next = page < total_pages
            has_previous = page > 1

            # Remover campos sensíveis de todos os registros
            for customer in customers:
                if 'password' in customer:
                    del customer['password']

            logger.info(f"[ListCustomersStrategy] Encontrados {len(customers)} clientes de {total_records} total")

            return response(200, {
                "message": "Clientes listados com sucesso",
                "customers": customers,
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
            logger.exception(f"[ListCustomersStrategy] Erro ao listar clientes: {e}")
            return response(500, {
                "message": f"Erro interno ao listar clientes: {str(e)}"
            })
