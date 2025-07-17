import pytest
import os
import sys

# Adiciona o diretório pai ao sys.path para permitir importações relativas


from resipaia import get_supabase_client, SupabaseSchema

# Lista de tabelas que esperamos que existam no Supabase
EXPECTED_TABLES = [
    SupabaseSchema.CADASTRO_PESSOAS_FISICA.name,
    SupabaseSchema.RECURSOS.name,
    SupabaseSchema.RESERVAS.name,
    SupabaseSchema.LISTA_ESPERA.name,
]

@pytest.fixture(scope="module")
def supabase_client():
    """Fixture para obter o cliente Supabase, garantindo que as credenciais estejam configuradas."""
    if "SUPABASE_URL" not in os.environ or "SUPABASE_KEY" not in os.environ:
        pytest.skip("Variáveis de ambiente SUPABASE_URL e SUPABASE_KEY não configuradas para testes de integração.")
    
    try:
        client = get_supabase_client()
        return client
    except Exception as e:
        pytest.fail(f"Falha ao obter cliente Supabase: {e}")

@pytest.mark.parametrize("table_name", EXPECTED_TABLES)
def test_table_exists_and_is_accessible(supabase_client, table_name):
    """Testa se cada tabela esperada existe e é acessível no Supabase."""
    try:
        # Tenta fazer uma consulta simples para verificar a existência da tabela
        # Limita a 1 registro para evitar carregar muitos dados
        response = supabase_client.from_(table_name).select("*").limit(1).execute()
        
        # Verifica se a resposta não contém erros de tabela inexistente ou permissão
        assert response.data is not None, f"Tabela '{table_name}' não retornou dados ou não existe."
        # O status code 200 (OK) ou 204 (No Content) indica sucesso na requisição
        assert response.status_code in [200, 204], f"Erro ao acessar a tabela '{table_name}': Status {response.status_code}"
        
        print(f"\n[INFO] Tabela '{table_name}' acessível com sucesso.")

    except Exception as e:
        pytest.fail(f"Erro ao acessar a tabela '{table_name}': {e}")
