import os
import psycopg2
import psycopg2.extras
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class DBClient:
    def __init__(self):
        # Parâmetros do SSM / Ambiente
        db_host_param = os.getenv("DB_HOST")
        db_user_param = os.getenv("DB_USER")
        db_password_param = os.getenv("DB_PASSWORD")
        db_name_param = os.getenv("DB_NAME")

        # Valida variáveis de ambiente
        if not all([db_host_param, db_user_param, db_password_param, db_name_param]):
            missing_vars = []
            if not db_host_param:
                missing_vars.append("DB_HOST")
            if not db_user_param:
                missing_vars.append("DB_USER")
            if not db_password_param:
                missing_vars.append("DB_PASSWORD")
            if not db_name_param:
                missing_vars.append("DB_NAME")
            raise ValueError(f"Variáveis de ambiente não configuradas: {', '.join(missing_vars)}")

        # Extrai host e porta (se vierem juntos)
        if ":" in db_host_param:
            db_host, db_port = db_host_param.split(":")
            db_port = int(db_port)
        else:
            db_host = db_host_param
            db_port = 5432  # padrão PostgreSQL

        logger.info(f"[DBClient] Conectando ao banco: host={db_host}, port={db_port}, dbname={db_name_param}")

        # Conexão PostgreSQL
        try:
            self._conn = psycopg2.connect(
                host=db_host,
                port=db_port,
                user=db_user_param,
                password=db_password_param,
                dbname=db_name_param
            )
            logger.info("[DBClient] Conexão PostgreSQL estabelecida com sucesso.")
        except Exception as e:
            logger.exception(f"[DBClient] Erro ao conectar no PostgreSQL: {str(e)}")
            raise ValueError(f"Erro ao conectar no PostgreSQL: {str(e)}")

    def execute(self, query, params=None):
        """Executa uma query de escrita (INSERT, UPDATE, DELETE)"""
        try:
            with self._conn.cursor() as cursor:
                cursor.execute(query, params)
            self._conn.commit()
            logger.info(f"[DBClient] Query executada com sucesso: {query}")
        except Exception as e:
            logger.exception(f"[DBClient] Erro ao executar query: {str(e)}")
            raise

    def fetch_one(self, query, params=None):
        """Executa uma query de leitura e retorna um único resultado como dicionário"""
        try:
            with self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(query, params)
                result = cursor.fetchone()
                logger.info(f"[DBClient] Query de leitura executada com sucesso: {query}")
                return dict(result) if result else None
        except Exception as e:
            logger.exception(f"[DBClient] Erro ao executar query de leitura: {str(e)}")
            raise

    def fetch_all(self, query, params=None):
        """Executa uma query de leitura e retorna múltiplos resultados como lista de dicionários"""
        try:
            with self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(query, params)
                results = cursor.fetchall()
                logger.info(f"[DBClient] Query de leitura executada com sucesso: {query}")
                return [dict(row) for row in results] if results else []
        except Exception as e:
            logger.exception(f"[DBClient] Erro ao executar query de leitura: {str(e)}")
            raise
