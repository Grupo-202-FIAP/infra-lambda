import json
from handler import handler

if __name__ == "__main__":
    event = {
        "body": json.dumps({
            "type": "internal",
            "email": "user@example.com",
            "password": "123456"
        })
    }

    context = None

    response = handler(event, context)
    print(json.dumps(response, indent=2))
