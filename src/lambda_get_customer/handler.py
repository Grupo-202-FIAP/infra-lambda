import json
import logging
from lambda_get_customer.strategies.get_customer_strategy import GetCustomerStrategy
from lambda_get_customer.utils.responses import response

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info("==== Iniciando execução da Lambda de busca de cliente ====")
    logger.info(f"Evento recebido: {json.dumps(event)}")

    try:
        # Tentar buscar parâmetros de query string (GET request)
        query_params = event.get("queryStringParameters", {})
        
        # Se não houver query params, tentar buscar do body (POST request)
        if not query_params or query_params is None:
            try:
                body = json.loads(event.get("body", "{}"))
                query_params = body
                logger.info(f"Parâmetros extraídos do body: {query_params}")
            except json.JSONDecodeError as e:
                logger.error(f"Erro ao decodificar body JSON: {e}")
                return response(400, {"message": "Corpo inválido: precisa ser JSON"})
        else:
            logger.info(f"Parâmetros extraídos de queryStringParameters: {query_params}")

        # Validar que pelo menos um parâmetro foi fornecido
        customer_id = query_params.get("customer_id")
        email = query_params.get("email")
        cpf = query_params.get("cpf")

        if not any([customer_id, email, cpf]):
            logger.warning("Nenhum parâmetro de busca fornecido")
            return response(400, {
                "message": "É necessário fornecer pelo menos um parâmetro de busca: customer_id, email ou cpf"
            })

        logger.info(f"Iniciando busca com parâmetros: customer_id={customer_id}, email={email}, cpf={cpf}")

        # Executar a estratégia de busca
        strategy = GetCustomerStrategy()
        result = strategy.execute(query_params)

        logger.info(f"Resultado da busca: {result}")
        logger.info("==== Execução concluída com sucesso ====")
        
        return result

    except ValueError as e:
        logger.warning(f"Erro de validação: {e}")
        return response(400, {"message": str(e)})

    except Exception as e:
        logger.exception(f"Erro inesperado durante a execução da Lambda: {e}")
        return response(500, {"message": f"Erro interno do servidor: {str(e)}"})
