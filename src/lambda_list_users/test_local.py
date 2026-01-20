import json
import os
from handler import handler

if __name__ == "__main__":
    os.environ["DB_HOST"] = "localhost:5432"
    os.environ["DB_USER"] = "postgres"
    os.environ["DB_PASSWORD"] = "postgres"
    os.environ["DB_NAME"] = "pos_db"
    os.environ["CUSTOMER_TABLE"] = "customers"
    os.environ["INTERNAL_TABLE"] = "internal_users"

    print("=== Teste 1: Listar primeira página (sem filtros) ===")
    event_1 = {
        "queryStringParameters": {
            "page": "1",
            "per_page": "10"
        },
        "body": None
    }
    response_1 = handler(event_1, None)
    print(json.dumps(response_1, indent=2, default=str))
    print()

    print("=== Teste 3: Filtrar por email ===")
    event_3 = {
        "queryStringParameters": {
            "email": "test",
            "page": "1",
            "per_page": "10"
        },
        "body": None
    }
    response_3 = handler(event_3, None)
    print(json.dumps(response_3, indent=2, default=str))
    print()

    print("=== Teste 4: Filtrar por status (aplica clientes) ===")
    event_4 = {
        "queryStringParameters": {
            "status": "active",
            "page": "1",
            "per_page": "10"
        },
        "body": None
    }
    response_4 = handler(event_4, None)
    print(json.dumps(response_4, indent=2, default=str))
    print()

    print("=== Teste 5: Sem parâmetros (usa defaults) ===")
    event_5 = {
        "queryStringParameters": None,
        "body": None
    }
    response_5 = handler(event_5, None)
    print(json.dumps(response_5, indent=2, default=str))
    print()
