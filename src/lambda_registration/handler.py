import json
import logging
from lambda_registration.strategies.customer_registration_strategy import CustomerRegistrationStrategy
from lambda_registration.strategies.internal_registration_strategy import InternalRegistrationStrategy
from lambda_registration.strategies.customer_sync import CustomerSyncStrategy
from lambda_registration.strategies.internal_sync import InternalSyncStrategy
from lambda_registration.utils.responses import response
from lambda_registration.utils.logger import get_logger

logger = logging.getLogger(__name__)

def handler(event, context):
    headers = event.get("headers") or {}
    correlation_id = headers.get("x-correlation-id") or headers.get("X-Correlation-Id")
    request_id = getattr(context, "aws_request_id", None)
    log = get_logger("lambda_registration", extra={"request_id": request_id, "correlation_id": correlation_id})

    log.info("==== Iniciando execução da Lambda de registro ====")
    log.info(f"Evento recebido: {json.dumps(event)}")

    # --- Caso 1: Evento veio do Cognito Trigger (PreSignUp) ---
    if "triggerSource" in event:
        log.info("Detectado evento Cognito Trigger. Retornando evento original.")
        
        # (Opcional) você pode confirmar o usuário automaticamente:
        event["response"]["autoConfirmUser"] = True
        event["response"]["autoVerifyEmail"] = True
        
        return event

    # --- Caso 2: Evento veio via API Gateway ---
    try:
        body = json.loads(event.get("body", "{}"))
        log.info(f"Body decodificado: {body}")
    except json.JSONDecodeError as e:
        log.error(f"Erro ao decodificar body JSON: {e}")
        return response(400, {"message": "Corpo inválido: precisa ser JSON"})

    user_type = body.get("type")
    if not user_type:
        log.warning("Campo 'type' ausente no body.")
        return response(400, {"message": "Campo 'type' obrigatório (ex: 'customer' ou 'internal')"})

    log.info(f"Tipo de usuário recebido: {user_type}")

    registration_map = {
        "customer": CustomerRegistrationStrategy,
        "internal": InternalRegistrationStrategy,
    }
    sync_map = {
        "customer": CustomerSyncStrategy,
        "internal": InternalSyncStrategy,
    }

    reg_class = registration_map.get(user_type)
    sync_class = sync_map.get(user_type)
    if not reg_class or not sync_class:
        log.error(f"Tipo de usuário inválido: {user_type}")
        return response(400, {"message": f"Tipo '{user_type}' inválido"})

    try:
        log.info(f"Iniciando registro para tipo '{user_type}' com strategy '{reg_class.__name__}'")
        reg_strategy = reg_class()
        reg_result = reg_strategy.execute(body)
        log.info(f"Resultado do registro: {reg_result}")
    except Exception as e:
        log.exception(f"Erro inesperado durante o registro: {e}")
        return response(500, {"message": f"Erro interno durante o registro: {str(e)}"})

    if reg_result.get("statusCode") != 201:
        log.warning(f"Registro falhou: {reg_result}")
        return reg_result

    try:
        log.info(f"Iniciando sync automático com strategy '{sync_class.__name__}'")
        sync_strategy = sync_class()

        reg_body = json.loads(reg_result["body"]) if reg_result.get("body") else {}
        sync_payload = {**body, "userId": reg_body.get("userId")}

        sync_result = sync_strategy.execute(sync_payload)
        log.info(f"Resultado do sync: {sync_result}")
    except Exception as e:
        log.exception(f"Erro inesperado durante o sync: {e}")
        return response(500, {"message": f"Erro interno durante o sync: {str(e)}"})

    result = response(201, {
        "message": f"{user_type.capitalize()} cadastrado e sincronizado com sucesso",
        "registration": json.loads(reg_result["body"]),
        "sync": json.loads(sync_result["body"]),
    })

    log.info(f"Resposta final da Lambda: {result}")
    log.info("==== Execução concluída com sucesso ====")
    return result
