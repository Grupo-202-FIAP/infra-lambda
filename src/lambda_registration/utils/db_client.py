import os
import json
import boto3
import psycopg2

class DBClient:
    def __init__(self):
        secret_name = os.getenv("DB_SECRET_NAME")
        if not secret_name:
            raise ValueError("DB_SECRET_NAME não configurado")

        sm = boto3.client("secretsmanager", region_name="us-east-1")
        secret_value = sm.get_secret_value(SecretId=secret_name)
        secret_dict = json.loads(secret_value["SecretString"])

        self._conn = psycopg2.connect(
            host=secret_dict["host"],
            user=secret_dict["username"],
            password=secret_dict["password"],
            dbname=secret_dict["dbname"]
        )

    def execute(self, query, params=None):
        with self._conn.cursor() as cursor:
            cursor.execute(query, params)
        self._conn.commit()