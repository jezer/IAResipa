import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Definição do esquema do Supabase
# Este arquivo mapeará as tabelas e colunas do Supabase para estruturas de dados Python.
# Pode ser uma classe, um dicionário, ou dataclasses para tipagem mais forte.

class SupabaseTable:
    def __init__(self, name: str, columns: list):
        self.name = name
        self.columns = columns

    def __repr__(self):
        return f"SupabaseTable(name='{self.name}', columns={self.columns})"

class SupabaseSchema:
    # Exemplo de mapeamento para a tabela 'cadastro_pessoas_fisica'
    CADASTRO_PESSOAS_FISICA = SupabaseTable(
        name="cadastro_pessoas_fisica",
        columns=["id", "phone_number", "name", "email", "created_at", "updated_at"]
    )

    # Exemplo de mapeamento para a tabela 'recursos' (quiosques, quadras)
    RECURSOS = SupabaseTable(
        name="recursos",
        columns=["id", "name", "type", "capacity", "location", "is_available"]
    )

    # Exemplo de mapeamento para a tabela 'reservas'
    RESERVAS = SupabaseTable(
        name="reservas",
        columns=["id", "user_id", "resource_id", "start_time", "end_time", "status", "pix_txid", "amount"]
    )

    # Exemplo de mapeamento para a tabela 'lista_espera'
    LISTA_ESPERA = SupabaseTable(
        name="lista_espera",
        columns=["id", "user_id", "resource_id", "requested_time", "status"]
    )

    @staticmethod
    def get_table_columns(table_name: str) -> list:
        if table_name == SupabaseSchema.CADASTRO_PESSOAS_FISICA.name:
            return SupabaseSchema.CADASTRO_PESSOAS_FISICA.columns
        elif table_name == SupabaseSchema.RECURSOS.name:
            return SupabaseSchema.RECURSOS.columns
        elif table_name == SupabaseSchema.RESERVAS.name:
            return SupabaseSchema.RESERVAS.columns
        elif table_name == SupabaseSchema.LISTA_ESPERA.name:
            return SupabaseSchema.LISTA_ESPERA.columns
        else:
            logging.warning(f"Tabela '{table_name}' não encontrada no esquema.")
            return []

if __name__ == "__main__":
    logging.info("Mapeamento do esquema do Supabase carregado.")
    logging.info(f"Colunas da tabela de usuários: {SupabaseSchema.get_table_columns('cadastro_pessoas_fisica')}")