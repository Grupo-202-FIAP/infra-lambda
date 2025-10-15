import json
from lambda_registration.strategies import (
    CustomerRegistrationStrategy,
    EmployeeRegistrationStrategy,
    CustomerSyncStrategy,
    EmployeeSyncStrategy,
)
from lambda_registration.utils.responses import response

def handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
    except json.JSONDecodeError:
        return response(400, {"message": "Corpo inválido: precisa ser JSON"})

    user_type = body.get("type")
    if not user_type:
        return response(400, {"message": "Campo 'type' obrigatório (ex: 'customer' ou 'employee')"})

    # Mapeia strategies por tipo
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
        return response(400, {"message": f"Tipo '{user_type}' inválido"})

    # Executa registro
    reg_strategy = reg_class()
    reg_result = reg_strategy.execute(body)

    if reg_result["statusCode"] != 201:
        # Se falhou no registro, não prossegue para o sync
        return reg_result

    # Executa sync automático
    sync_strategy = sync_class()
    sync_result = sync_strategy.execute(body)

    # Retorna resultado consolidado
    return response(201, {
        "message": f"{user_type.capitalize()} cadastrado e sincronizado com sucesso",
        "registration": json.loads(reg_result["body"]),
        "sync": json.loads(sync_result["body"]),
    })
