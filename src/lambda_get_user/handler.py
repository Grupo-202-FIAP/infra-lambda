import json
import logging
from lambda_get_user.strategies.get_user_strategy import GetUserStrategy
from lambda_get_user.utils.responses import response
from lambda_get_user.utils.logger import get_logger

logger = logging.getLogger(__name__)


def handler(event, context):
    headers = event.get("headers") or {}
    correlation_id = headers.get("x-correlation-id") or headers.get("X-Correlation-Id")
    request_id = getattr(context, "aws_request_id", None)
    log = get_logger("lambda_get_user", extra={"request_id": request_id, "correlation_id": correlation_id})

    log.info("==== Iniciando execução da Lambda de busca de usuário ====")
    log.info(f"Evento recebido: {json.dumps(event)}")

    try:
        query_params = event.get("queryStringParameters", {})

        if not query_params or query_params is None:
            try:
                body = json.loads(event.get("body", "{}"))
                query_params = body
                log.info(f"Parâmetros extraídos do body: {query_params}")
            except json.JSONDecodeError as e:
                log.error(f"Erro ao decodificar body JSON: {e}")
                return response(400, {"message": "Corpo inválido: precisa ser JSON"})
        else:
            log.info(f"Parâmetros extraídos de queryStringParameters: {query_params}")

        # Compatibilidade de nomes de parâmetros
        uid = query_params.get("user_id") or query_params.get("id") or query_params.get("customer_id")
        email = query_params.get("email")
        cpf = query_params.get("cpf")

        if not any([uid, email, cpf]):
            log.warning("Nenhum parâmetro de busca fornecido")
            return response(400, {
                "message": "É necessário fornecer pelo menos um parâmetro de busca: user_id/id/customer_id, email ou cpf"
            })

        log.info(f"Iniciando busca com parâmetros: user_id={uid}, email={email}, cpf={cpf}")

        strategy = GetUserStrategy()
        result = strategy.execute(query_params)

        log.info(f"Resultado da busca: {result}")
        log.info("==== Execução concluída com sucesso ====")

        return result

    except ValueError as e:
        log.warning(f"Erro de validação: {e}")
        return response(400, {"message": str(e)})

    except Exception as e:
        log.exception(f"Erro inesperado durante a execução da Lambda: {e}")
        return response(500, {"message": f"Erro interno do servidor: {str(e)}"})
