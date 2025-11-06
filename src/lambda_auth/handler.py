import os
from lambda_auth.utils.responses import response
from lambda_auth.utils.json_parser import parse_json_body
from lambda_auth.strategies.internal_auth import InternalAuthStrategy
from lambda_auth.strategies.customer_auth import CustomerAuthStrategy

class AuthFactory:
    STRATEGIES = {
        "internal": InternalAuthStrategy(),
        "customer": CustomerAuthStrategy()
    }

    @classmethod
    def get_strategy(cls, user_type):
        return cls.STRATEGIES.get(user_type)

def handler(event, context):
    try:
        body = parse_json_body(event)
        user_type = body.get("type")

        if not user_type:
            return response(400, {"message": "Campo 'type' obrigatório (ex: internal ou customer)"})

        strategy = AuthFactory.get_strategy(user_type)
        if not strategy:
            return response(400, {"message": f"Tipo '{user_type}' não suportado"})

        return strategy.authenticate(body)

    except ValueError as e:
        return response(400, {"message": str(e)})
    except Exception as e:
        return response(500, {"message": f"Erro interno do servidor: {e}"})
