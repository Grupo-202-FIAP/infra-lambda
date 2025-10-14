import json

def parse_json_body(event):
    try:
        return json.loads(event.get("body", "{}"))
    except json.JSONDecodeError:
        raise ValueError("Corpo inválido: precisa ser JSON")
