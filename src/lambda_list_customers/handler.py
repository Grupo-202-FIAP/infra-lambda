import json
import logging
from lambda_list_customers.strategies.list_customers_strategy import ListCustomersStrategy
from lambda_list_customers.utils.responses import response

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info("==== Iniciando execução da Lambda de listagem de clientes ====")
    logger.info(f"Evento recebido: {json.dumps(event)}")

    try:
        # Extrair parâmetros de query string (GET request)
        query_params = event.get("queryStringParameters") or {}
        logger.info(f"Parâmetros extraídos: {query_params}")

        # Se não houver query params, tentar buscar do body (POST request)
        if not query_params or query_params == {}:
            try:
                body = json.loads(event.get("body", "{}"))
                query_params = body
                logger.info(f"Parâmetros extraídos do body: {query_params}")
            except json.JSONDecodeError as e:
                logger.error(f"Erro ao decodificar body JSON: {e}")
                return response(400, {"message": "Corpo inválido: precisa ser JSON"})

        # Executar a estratégia de listagem
        strategy = ListCustomersStrategy()
        result = strategy.execute(query_params)

        logger.info(f"Resultado da listagem: statusCode={result.get('statusCode')}")
        logger.info("==== Execução concluída com sucesso ====")
        
        return result

    except ValueError as e:
        logger.warning(f"Erro de validação: {e}")
        return response(400, {"message": str(e)})

    except Exception as e:
        logger.exception(f"Erro inesperado durante a execução da Lambda: {e}")
        return response(500, {"message": f"Erro interno do servidor: {str(e)}"})
