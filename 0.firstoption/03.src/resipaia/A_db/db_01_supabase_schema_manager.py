import os
import psycopg2
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_pg_connection():
    """Obtém uma conexão com o banco de dados PostgreSQL do Supabase."""
    pg_host = os.environ.get("PG_HOST")
    pg_port = os.environ.get("PG_PORT", "5432")
    pg_dbname = os.environ.get("PG_DBNAME")
    pg_user = os.environ.get("PG_USER")
    pg_password = os.environ.get("PG_PASSWORD")

    if not all([pg_host, pg_dbname, pg_user, pg_password]):
        logging.error("Variáveis de ambiente PG_HOST, PG_DBNAME, PG_USER, PG_PASSWORD não configuradas.")
        raise ValueError("Credenciais do PostgreSQL não configuradas.")

    try:
        conn = psycopg2.connect(
            host=pg_host,
            port=pg_port,
            dbname=pg_dbname,
            user=pg_user,
            password=pg_password
        )
        logging.info("Conexão PostgreSQL estabelecida com sucesso.")
        return conn
    except Exception as e:
        logging.error(f"Erro ao conectar ao PostgreSQL: {e}")
        raise

def create_test_table(conn, table_name="test_table"):
    """Cria a tabela de teste no esquema public, se ela não existir."""
    try:
        with conn.cursor() as cur:
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS public.{table_name} (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    name TEXT,
                    email TEXT UNIQUE
                );
            """)
            conn.commit()
            logging.info(f"Tabela '{table_name}' criada ou já existe no esquema public.")
    except Exception as e:
        conn.rollback()
        logging.error(f"Erro ao criar a tabela '{table_name}': {e}")
        raise

def drop_test_table(conn, table_name="test_table"):
    """Exclui a tabela de teste do esquema public, se ela existir."""
    try:
        with conn.cursor() as cur:
            cur.execute(f"""
                DROP TABLE IF EXISTS public.{table_name} CASCADE;
            """)
            conn.commit()
            logging.info(f"Tabela '{table_name}' excluída do esquema public.")
    except Exception as e:
        conn.rollback()
        logging.error(f"Erro ao excluir a tabela '{table_name}': {e}")
        raise

if __name__ == "__main__":
    # Exemplo de uso:
    conn = None
    try:
        conn = get_pg_connection()
        
        # Criar a tabela de teste
        create_test_table(conn)

        # Você pode adicionar mais funções aqui para criar outros objetos, índices, etc.
        # Exemplo: create_index(conn, "test_table", "email")

        logging.info("Operações de esquema concluídas com sucesso.")

    except Exception as e:
        logging.error(f"Falha nas operações de esquema: {e}")
    finally:
        if conn:
            conn.close()
            logging.info("Conexão PostgreSQL fechada.")
