import os
import logging
from lambda_get_customer.strategies.base import BaseStrategy
from lambda_get_customer.utils.db_client import DBClient
from lambda_get_customer.utils.responses import response

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class GetCustomerStrategy(BaseStrategy):
    def __init__(self, db_client: DBClient = None):
        self.db = db_client or DBClient()
        self.table_name = os.getenv("CUSTOMER_TABLE", "customers")

    def execute(self, data):
        logger.info(f"[GetCustomerStrategy] Iniciando busca de cliente com dados: {data}")

        # Validar parâmetros de busca
        customer_id = data.get("customer_id")
        email = data.get("email")
        cpf = data.get("cpf")

        # Pelo menos um parâmetro deve ser fornecido
        if not any([customer_id, email, cpf]):
            logger.warning("[GetCustomerStrategy] Nenhum parâmetro de busca fornecido")
            return response(400, {
                "message": "É necessário fornecer pelo menos um parâmetro de busca: customer_id, email ou cpf"
            })

        # Construir query baseado nos parâmetros fornecidos
        query_conditions = []
        query_params = []

        if customer_id:
            query_conditions.append("id = %s")
            query_params.append(customer_id)
        
        if email:
            query_conditions.append("email = %s")
            query_params.append(email)
        
        if cpf:
            query_conditions.append("cpf = %s")
            query_params.append(cpf)

        # Montar a query completa
        where_clause = " AND ".join(query_conditions)
        query = f"SELECT * FROM {self.table_name} WHERE {where_clause} LIMIT 1"

        try:
            logger.info(f"[GetCustomerStrategy] Executando query: {query}")
            customer = self.db.fetch_one(query, tuple(query_params))

            if not customer:
                logger.info("[GetCustomerStrategy] Cliente não encontrado")
                return response(404, {
                    "message": "Cliente não encontrado"
                })

            # Verificar se é realmente um CUSTOMER (caso haja campo de tipo)
            # Alguns bancos podem ter um campo 'user_type' ou similar
            # Por enquanto, assumimos que a tabela 'customers' só contém CUSTOMER

            logger.info(f"[GetCustomerStrategy] Cliente encontrado: {customer.get('email')}")
            
            # Remover campos sensíveis se necessário
            # Por exemplo: remover senha ou tokens
            if 'password' in customer:
                del customer['password']

            return response(200, {
                "message": "Cliente encontrado com sucesso",
                "customer": customer
            })

        except Exception as e:
            logger.exception(f"[GetCustomerStrategy] Erro ao buscar cliente: {e}")
            return response(500, {
                "message": f"Erro interno ao buscar cliente: {str(e)}"
            })
