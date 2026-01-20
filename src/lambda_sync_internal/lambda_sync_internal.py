import os
import json
import psycopg2
import boto3

SECRET_NAME = os.environ.get("DB_SECRET_NAME")
REGION_NAME = os.environ.get("AWS_REGION", "us-east-1")

def handler(event, context):
    print("Evento recebido:", json.dumps(event))

    user_attrs = event["request"]["userAttributes"]
    user_id = user_attrs.get("sub")
    email = user_attrs.get("email")
    name = user_attrs.get("name")

    if not email:
        print("Usuário sem email, ignorando...")
        return event

    secrets_client = boto3.client("secretsmanager", region_name=REGION_NAME)
    secret_value = secrets_client.get_secret_value(SecretId=SECRET_NAME)
    secret_dict = json.loads(secret_value["SecretString"])

    db_host = secret_dict["host"]
    db_user = secret_dict["username"]
    db_pass = secret_dict["password"]
    db_name = secret_dict["dbname"]

    connection = psycopg2.connect(
        host=db_host,
        user=db_user,
        password=db_pass,
        database=db_name,
        connect_timeout=5
    )

    try:
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO usuarios (id_cognito, nome, email)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE nome = VALUES(nome), email = VALUES(email);
            """
            cursor.execute(sql, (user_id, name, email))
            connection.commit()
            print(f"Usuário {email} inserido/atualizado com sucesso no banco.")
    except Exception as e:
        print("Erro ao inserir usuário:", str(e))
        raise e
    finally:
        connection.close()

    return event
