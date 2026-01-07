import os
import psycopg2
import psycopg2.extras
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
            if ":" in self._db_host_param:
                db_host, db_port = self._db_host_param.split(":")
                db_port = int(db_port)
            else:
                db_host = self._db_host_param
                db_port = 5432

            logger.info(f"[DBClient] Conectando ao banco: host={db_host}, port={db_port}, dbname={self._db_name_param}")

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

    def fetch_one(self, query, params=None):
        try:
            conn = self._get_connection()
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(query, params)
                result = cursor.fetchone()
                logger.info(f"[DBClient] Query de leitura executada com sucesso: {query}")
                return dict(result) if result else None
        except Exception as e:
            logger.exception(f"[DBClient] Erro ao executar query de leitura: {str(e)}")
            raise

    def fetch_all(self, query, params=None):
        try:
            conn = self._get_connection()
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(query, params)
                results = cursor.fetchall()
                logger.info(f"[DBClient] Query de leitura executada com sucesso: {query}")
                return [dict(row) for row in results] if results else []
        except Exception as e:
            logger.exception(f"[DBClient] Erro ao executar query de leitura: {str(e)}")
            raise
