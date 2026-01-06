import json
import os
from handler import handler

if __name__ == "__main__":
    # Configurar variáveis de ambiente para teste local
    os.environ["DB_HOST"] = "localhost:5432"
    os.environ["DB_USER"] = "postgres"
    os.environ["DB_PASSWORD"] = "postgres"
    os.environ["DB_NAME"] = "pos_db"
    os.environ["CUSTOMER_TABLE"] = "customers"

    # Teste 1: Buscar por customer_id via query params
    print("=== Teste 1: Buscar por customer_id (query params) ===")
    event_1 = {
        "queryStringParameters": {
            "customer_id": "1"
        },
        "body": None
    }
    response_1 = handler(event_1, None)
    print(json.dumps(response_1, indent=2))
    print()

    # Teste 2: Buscar por email via body
    print("=== Teste 2: Buscar por email (body) ===")
    event_2 = {
        "queryStringParameters": None,
        "body": json.dumps({
            "email": "customer@example.com"
        })
    }
    response_2 = handler(event_2, None)
    print(json.dumps(response_2, indent=2))
    print()

    # Teste 3: Buscar por CPF
    print("=== Teste 3: Buscar por CPF ===")
    event_3 = {
        "queryStringParameters": {
            "cpf": "12345678900"
        },
        "body": None
    }
    response_3 = handler(event_3, None)
    print(json.dumps(response_3, indent=2))
    print()

    # Teste 4: Sem parâmetros (deve retornar 400)
    print("=== Teste 4: Sem parâmetros (esperado 400) ===")
    event_4 = {
        "queryStringParameters": None,
        "body": "{}"
    }
    response_4 = handler(event_4, None)
    print(json.dumps(response_4, indent=2))
    print()

    # Teste 5: Cliente não encontrado (deve retornar 404)
    print("=== Teste 5: Cliente não encontrado (esperado 404) ===")
    event_5 = {
        "queryStringParameters": {
            "customer_id": "999999"
        },
        "body": None
    }
    response_5 = handler(event_5, None)
    print(json.dumps(response_5, indent=2))
