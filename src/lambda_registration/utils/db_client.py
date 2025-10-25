import os
import boto3
import psycopg2

class DBClient:
    def __init__(self):
        # Parâmetros do SSM Parameter Store (passados via infraestrutura)
        db_host_param = os.getenv("DB_HOST")
        db_user_param = os.getenv("DB_USER")
        db_password_param = os.getenv("DB_PASSWORD")
        db_name = os.getenv("DB_NAME")
        
        # Validar se as variáveis de ambiente foram definidas
        if not all([db_host_param, db_user_param, db_password_param, db_name]):
            missing_vars = []
            if not db_host_param: missing_vars.append("DB_HOST")
            if not db_user_param: missing_vars.append("DB_USER")
            if not db_password_param: missing_vars.append("DB_PASSWORD")
            if not db_name: missing_vars.append("DB_NAME")
            raise ValueError(f"Variáveis de ambiente não configuradas: {', '.join(missing_vars)}")
        
        # Cliente SSM
        ssm = boto3.client("ssm", region_name="us-east-1")
        
        try:
            # Buscar parâmetros do SSM
            user_response = ssm.get_parameter(Name=db_user_param)
            password_response = ssm.get_parameter(Name=db_password_param, WithDecryption=True)
            
            db_user = user_response["Parameter"]["Value"]
            db_password = password_response["Parameter"]["Value"]
            
        except Exception as e:
            raise ValueError(f"Erro ao buscar parâmetros do SSM: {str(e)}")

        self._conn = psycopg2.connect(
            host=db_host_param,
            user=db_user,
            password=db_password,
            dbname=db_name
        )

    def execute(self, query, params=None):
        with self._conn.cursor() as cursor:
            cursor.execute(query, params)
        self._conn.commit()