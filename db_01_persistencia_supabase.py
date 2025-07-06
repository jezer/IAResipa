from supabase import create_client
from supabase_config import SUPABASE_URL, SUPABASE_KEY

class PersistenciaSupabase:
    def __init__(self):
        self.client = create_client(SUPABASE_URL, SUPABASE_KEY)

    def criar_tabela(self, sql: str):
        self.client.rpc("execute_sql", {"sql": sql}).execute()

    def inserir(self, tabela: str, dados: dict):
        return self.client.table(tabela).insert(dados).execute()