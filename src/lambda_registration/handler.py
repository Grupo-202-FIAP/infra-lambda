import json
import logging
from lambda_registration.strategies.customer_registration_strategy import CustomerRegistrationStrategy
from lambda_registration.strategies.employee_registration_strategy import EmployeeRegistrationStrategy
from lambda_registration.strategies.customer_sync import CustomerSyncStrategy
from lambda_registration.strategies.employee_sync import EmployeeSyncStrategy
from lambda_registration.utils.responses import response

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    logger.info("==== Iniciando execução da Lambda de registro ====")
    logger.info(f"Evento recebido: {json.dumps(event)}")

    # --- Caso 1: Evento veio do Cognito Trigger (PreSignUp) ---
    if "triggerSource" in event:
        logger.info("Detectado evento Cognito Trigger. Retornando evento original.")
        
        # (Opcional) você pode confirmar o usuário automaticamente:
        event["response"]["autoConfirmUser"] = True
        event["response"]["autoVerifyEmail"] = True
        
        return event

    # --- Caso 2: Evento veio via API Gateway ---
    try:
        body = json.loads(event.get("body", "{}"))
        logger.info(f"Body decodificado: {body}")
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar body JSON: {e}")
        return response(400, {"message": "Corpo inválido: precisa ser JSON"})

    user_type = body.get("type")
    if not user_type:
        logger.warning("Campo 'type' ausente no body.")
        return response(400, {"message": "Campo 'type' obrigatório (ex: 'customer' ou 'employee')"})

    logger.info(f"Tipo de usuário recebido: {user_type}")

    registration_map = {
        "customer": CustomerRegistrationStrategy,
        "employee": EmployeeRegistrationStrategy,
    }
    sync_map = {
        "customer": CustomerSyncStrategy,
        "employee": EmployeeSyncStrategy,
    }

    reg_class = registration_map.get(user_type)
    sync_class = sync_map.get(user_type)
    if not reg_class or not sync_class:
        logger.error(f"Tipo de usuário inválido: {user_type}")
        return response(400, {"message": f"Tipo '{user_type}' inválido"})

    try:
        logger.info(f"Iniciando registro para tipo '{user_type}' com strategy '{reg_class.__name__}'")
        reg_strategy = reg_class()
        reg_result = reg_strategy.execute(body)
        logger.info(f"Resultado do registro: {reg_result}")
    except Exception as e:
        logger.exception(f"Erro inesperado durante o registro: {e}")
        return response(500, {"message": f"Erro interno durante o registro: {str(e)}"})

    if reg_result.get("statusCode") != 201:
        logger.warning(f"Registro falhou: {reg_result}")
        return reg_result

    try:
        logger.info(f"Iniciando sync automático com strategy '{sync_class.__name__}'")
        sync_strategy = sync_class()
        sync_result = sync_strategy.execute(body)
        logger.info(f"Resultado do sync: {sync_result}")
    except Exception as e:
        logger.exception(f"Erro inesperado durante o sync: {e}")
        return response(500, {"message": f"Erro interno durante o sync: {str(e)}"})

    result = response(201, {
        "message": f"{user_type.capitalize()} cadastrado e sincronizado com sucesso",
        "registration": json.loads(reg_result["body"]),
        "sync": json.loads(sync_result["body"]),
    })

    logger.info(f"Resposta final da Lambda: {result}")
    logger.info("==== Execução concluída com sucesso ====")
    return result
