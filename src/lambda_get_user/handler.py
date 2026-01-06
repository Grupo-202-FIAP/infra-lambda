import json
import logging
from lambda_get_user.strategies.get_user_strategy import GetUserStrategy
from lambda_get_user.utils.responses import response

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info("==== Iniciando execução da Lambda de busca de usuário ====")
    logger.info(f"Evento recebido: {json.dumps(event)}")

    try:
        query_params = event.get("queryStringParameters", {})

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

        # Compatibilidade de nomes de parâmetros
        uid = query_params.get("user_id") or query_params.get("id") or query_params.get("customer_id")
        email = query_params.get("email")
        cpf = query_params.get("cpf")

        if not any([uid, email, cpf]):
            logger.warning("Nenhum parâmetro de busca fornecido")
            return response(400, {
                "message": "É necessário fornecer pelo menos um parâmetro de busca: user_id/id/customer_id, email ou cpf"
            })

        logger.info(f"Iniciando busca com parâmetros: user_id={uid}, email={email}, cpf={cpf}")

        strategy = GetUserStrategy()
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
