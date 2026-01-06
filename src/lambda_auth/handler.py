import os
import json
import logging
from lambda_auth.utils.responses import response
from lambda_auth.utils.json_parser import parse_json_body
from lambda_auth.strategies.internal_auth import InternalAuthStrategy
from lambda_auth.strategies.customer_auth import CustomerAuthStrategy

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class AuthFactory:
    STRATEGIES = {
        "internal": InternalAuthStrategy(),
        "customer": CustomerAuthStrategy()
    }

    @classmethod
    def get_strategy(cls, user_type):
        return cls.STRATEGIES.get(user_type)


def handler(event, context):
    logger.info("==== Iniciando execução da Lambda de autenticação ====")
    logger.info(f"Evento recebido: {json.dumps(event)}")

    try:
        body = parse_json_body(event)
        logger.info(f"Body decodificado: {body}")

        user_type = body.get("type")
        if not user_type:
            logger.warning("Campo 'type' ausente no body.")
            return response(400, {"message": "Campo 'type' obrigatório (ex: internal ou customer)"})

        logger.info(f"Tipo de usuário recebido: {user_type}")

        strategy = AuthFactory.get_strategy(user_type)
        if not strategy:
            logger.error(f"Tipo de autenticação inválido: {user_type}")
            return response(400, {"message": f"Tipo '{user_type}' não suportado"})

        logger.info(f"Iniciando autenticação com strategy '{strategy.__class__.__name__}'")
        result = strategy.authenticate(body)
        logger.info(f"Resultado da autenticação: {result}")

        logger.info("==== Execução concluída com sucesso ====")
        return result

    except ValueError as e:
        logger.warning(f"Erro de validação: {e}")
        return response(400, {"message": str(e)})

    except Exception as e:
        logger.exception(f"Erro inesperado durante a execução da Lambda: {e}")
        return response(500, {"message": f"Erro interno do servidor: {e}"})