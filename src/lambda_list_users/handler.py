import json
import logging
from lambda_list_users.strategies.list_users_strategy import ListUsersStrategy
from lambda_list_users.utils.responses import response
from lambda_list_users.utils.logger import get_logger

logger = logging.getLogger(__name__)


def handler(event, context):
    headers = event.get("headers") or {}
    correlation_id = headers.get("x-correlation-id") or headers.get("X-Correlation-Id")
    request_id = getattr(context, "aws_request_id", None)
    log = get_logger("lambda_list_users", extra={"request_id": request_id, "correlation_id": correlation_id})

    log.info("==== Iniciando execução da Lambda de listagem de usuários ====")
    log.info(f"Evento recebido: {json.dumps(event)}")

    try:
        query_params = event.get("queryStringParameters") or {}
        log.info(f"Parâmetros extraídos: {query_params}")

        if not query_params or query_params == {}:
            try:
                body = json.loads(event.get("body", "{}"))
                query_params = body
                log.info(f"Parâmetros extraídos do body: {query_params}")
            except json.JSONDecodeError as e:
                log.error(f"Erro ao decodificar body JSON: {e}")
                return response(400, {"message": "Corpo inválido: precisa ser JSON"})

        strategy = ListUsersStrategy()
        result = strategy.execute(query_params)

        log.info(f"Resultado da listagem: statusCode={result.get('statusCode')}")
        log.info("==== Execução concluída com sucesso ====")

        return result

    except ValueError as e:
        log.warning(f"Erro de validação: {e}")
        return response(400, {"message": str(e)})

    except Exception as e:
        log.exception(f"Erro inesperado durante a execução da Lambda: {e}")
        return response(500, {"message": f"Erro interno do servidor: {str(e)}"})
