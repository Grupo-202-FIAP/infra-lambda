import json
from handler import handler

if __name__ == "__main__":
    event = {
        "body": json.dumps({
            "type": "customer",
            "cpf": "12345678900"
        })
    }

    context = None

    response = handler(event, context)
    print(json.dumps(response, indent=2))
