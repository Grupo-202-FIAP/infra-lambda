import os
import json
import logging
from lambda_auth.utils.responses import response
from lambda_auth.utils.json_parser import parse_json_body
from lambda_auth.strategies.internal_auth import InternalAuthStrategy
from lambda_auth.strategies.customer_auth import CustomerAuthStrategy
from lambda_auth.utils.logger import get_logger

logger = logging.getLogger(__name__)

class AuthFactory:
    STRATEGIES = {
        "internal": InternalAuthStrategy(),
        "customer": CustomerAuthStrategy()
    }

    @classmethod
    def get_strategy(cls, user_type):
        return cls.STRATEGIES.get(user_type)


def handler(event, context):
    headers = event.get("headers") or {}
    correlation_id = headers.get("x-correlation-id") or headers.get("X-Correlation-Id")
    request_id = getattr(context, "aws_request_id", None)
    log = get_logger("lambda_auth", extra={"request_id": request_id, "correlation_id": correlation_id})

    log.info("==== Iniciando execução da Lambda de autenticação ====")
    log.info(f"Evento recebido: {json.dumps(event)}")

    try:
        body = parse_json_body(event)
        log.info(f"Body decodificado: {body}")

        user_type = body.get("type")
        if not user_type:
            log.warning("Campo 'type' ausente no body.")
            return response(400, {"message": "Campo 'type' obrigatório (ex: internal ou customer)"})

        log.info(f"Tipo de usuário recebido: {user_type}")

        strategy = AuthFactory.get_strategy(user_type)
        if not strategy:
            log.error(f"Tipo de autenticação inválido: {user_type}")
            return response(400, {"message": f"Tipo '{user_type}' não suportado"})

        log.info(f"Iniciando autenticação com strategy '{strategy.__class__.__name__}'")
        result = strategy.authenticate(body)
        log.info(f"Resultado da autenticação: {result}")

        log.info("==== Execução concluída com sucesso ====")
        return result

    except ValueError as e:
        log.warning(f"Erro de validação: {e}")
        return response(400, {"message": str(e)})

    except Exception as e:
        log.exception(f"Erro inesperado durante a execução da Lambda: {e}")
        return response(500, {"message": f"Erro interno do servidor: {e}"})