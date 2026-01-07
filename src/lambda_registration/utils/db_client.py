import os
import boto3
import psycopg2
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class DBClient:
    def __init__(self):
        # Armazena parâmetros do ambiente sem conectar ainda (lazy connection)
        self._db_host_param = os.getenv("DB_HOST")
        self._db_user_param = os.getenv("DB_USER")
        self._db_password_param = os.getenv("DB_PASSWORD")
        self._db_name_param = os.getenv("DB_NAME")

        # Valida variáveis de ambiente
        if not all([self._db_host_param, self._db_user_param, self._db_password_param, self._db_name_param]):
            missing_vars = []
            if not self._db_host_param:
                missing_vars.append("DB_HOST")
            if not self._db_user_param:
                missing_vars.append("DB_USER")
            if not self._db_password_param:
                missing_vars.append("DB_PASSWORD")
            if not self._db_name_param:
                missing_vars.append("DB_NAME")
            raise ValueError(f"Variáveis de ambiente não configuradas: {', '.join(missing_vars)}")

        # Conexão será estabelecida sob demanda
        self._conn = None
        logger.info("[DBClient] Inicializado (conexão será feita sob demanda)")

    def _get_connection(self):
        """Lazy connection - apenas conecta quando necessário"""
        if self._conn is None:
            # Extrai host e porta (se vierem juntos)
            if ":" in self._db_host_param:
                db_host, db_port = self._db_host_param.split(":")
                db_port = int(db_port)
            else:
                db_host = self._db_host_param
                db_port = 5432  # padrão PostgreSQL

            logger.info(f"[DBClient] Conectando ao banco: host={db_host}, port={db_port}, dbname={self._db_name_param}")

            # Conexão PostgreSQL
            try:
                self._conn = psycopg2.connect(
                    host=db_host,
                    port=db_port,
                    user=self._db_user_param,
                    password=self._db_password_param,
                    dbname=self._db_name_param
                )
                logger.info("[DBClient] Conexão PostgreSQL estabelecida com sucesso.")
            except Exception as e:
                logger.exception(f"[DBClient] Erro ao conectar no PostgreSQL: {str(e)}")
                raise ValueError(f"Erro ao conectar no PostgreSQL: {str(e)}")
        
        return self._conn

    def execute(self, query, params=None):
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(query, params)
            conn.commit()
            logger.info(f"[DBClient] Query executada com sucesso: {query}")
        except Exception as e:
            logger.exception(f"[DBClient] Erro ao executar query: {str(e)}")
            raise
