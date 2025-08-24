import pytest
import os
import uuid
from supabase import Client

# Importar as funções do seu projeto
from resipaia import get_supabase_client, supabase_crud

@pytest.fixture(scope="module")
def supabase_client():
    """Fixture para obter o cliente Supabase, garantindo que as credenciais estejam configuradas."""
    # As credenciais são carregadas via .env e db_00_supabase_config.py
    try:
        client = get_supabase_client()
        return client
    except Exception as e:
        pytest.fail(f"Falha ao obter cliente Supabase: {e}")

@pytest.fixture(scope="function")
def temp_table_name(supabase_client: Client):
    """Fixture para criar e limpar uma tabela temporária para cada função de teste."""
    table_name = f"test_gemini_crud_{uuid.uuid4().hex}"
    
    # Criar a tabela temporária (assumindo que o RLS permite)
    # No Supabase, a criação de tabelas via cliente não é direta. 
    # Para testes, podemos simular ou usar uma tabela pré-existente.
    # Para este teste, vamos usar uma tabela que sabemos que existe e 
    # que foi criada pelo script create_tables.sql (ex: 'recursos')
    # e apenas inserir/deletar dados nela.
    # No entanto, para um teste de integração mais isolado, o ideal seria
    # ter permissão para criar e dropar tabelas temporárias.
    # Por simplicidade, vamos usar 'recursos' e limpar os dados inseridos.
    
    yield table_name

    # Limpar: deletar os dados inseridos na tabela temporária
    try:
        # Deleta todos os registros da tabela temporária que foram criados pelo teste
        # Isso é crucial para não poluir o banco de dados de teste.
        supabase_client.from_(table_name).delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        print(f"\n[INFO] Limpeza de dados da tabela temporária: {table_name}")
    except Exception as e:
        print(f"\n[WARNING] Não foi possível limpar a tabela temporária {table_name}: {e}")

def test_supabase_crud_insert(supabase_client: Client, temp_table_name: str):
    """Testa a operação de INSERT via supabase_crud."""
    # Usando a tabela 'recursos' para o teste
    table_to_use = "recursos"
    test_data = {"name": f"Recurso Teste Insert {uuid.uuid4().hex[:4]}", "type": "sala", "capacity": 5, "location": "bloco A", "is_available": True}
    
    print(f"\n[INFO] Inserindo dados em {table_to_use}: {test_data}")
    response = supabase_crud(supabase_client, action="insert", table=table_to_use, data=test_data)
    
    assert response["status"] == "success", f"Falha no INSERT: {response.get("message", "")}"
    assert response["data"] is not None, "INSERT não retornou dados."
    assert len(response["data"]) > 0, "INSERT retornou lista vazia."
    
    inserted_id = response["data"][0]['id']
    print(f"✅ INSERT OK | ID: {inserted_id}")

    # Limpeza específica para este teste
    try:
        supabase_client.from_(table_to_use).delete().eq("id", inserted_id).execute()
    except Exception as e:
        print(f"[WARNING] Falha na limpeza do INSERT: {e}")

def test_supabase_crud_select(supabase_client: Client, temp_table_name: str):
    """Testa a operação de SELECT via supabase_crud."""
    table_to_use = "recursos"
    test_data = {"name": f"Recurso Teste Select {uuid.uuid4().hex[:4]}", "type": "sala", "capacity": 5, "location": "bloco B", "is_available": True}
    
    # Inserir um item para poder selecioná-lo
    insert_response = supabase_crud(supabase_client, action="insert", table=table_to_use, data=test_data)
    assert insert_response["status"] == "success"
    inserted_id = insert_response["data"][0]['id']

    print(f"\n[INFO] Selecionando dados de {table_to_use} com ID: {inserted_id}")
    response = supabase_crud(supabase_client, action="select", table=table_to_use, query={"id": inserted_id})

    assert response["status"] == "success", f"Falha no SELECT: {response.get("message", "")}"
    assert response["data"] is not None, "SELECT não retornou dados."
    assert len(response["data"]) == 1, "SELECT retornou número inesperado de registros."
    assert response["data"][0]['name'] == test_data['name'], "Dados selecionados não correspondem."
    print(f"✅ SELECT OK | Nome: {response["data"][0]['name']}")

    # Limpeza específica para este teste
    try:
        supabase_client.from_(table_to_use).delete().eq("id", inserted_id).execute()
    except Exception as e:
        print(f"[WARNING] Falha na limpeza do SELECT: {e}")

def test_supabase_crud_update(supabase_client: Client, temp_table_name: str):
    """Testa a operação de UPDATE via supabase_crud."""
    table_to_use = "recursos"
    test_data = {"name": f"Recurso Teste Update {uuid.uuid4().hex[:4]}", "type": "sala", "capacity": 5, "location": "bloco C", "is_available": True}
    
    # Inserir um item para poder atualizá-lo
    insert_response = supabase_crud(supabase_client, action="insert", table=table_to_use, data=test_data)
    assert insert_response["status"] == "success"
    inserted_id = insert_response["data"][0]['id']

    updated_data = {"capacity": 10}
    print(f"\n[INFO] Atualizando dados em {table_to_use} para ID: {inserted_id} com {updated_data}")
    response = supabase_crud(supabase_client, action="update", table=table_to_use, data=updated_data, query={"id": inserted_id})

    assert response["status"] == "success", f"Falha no UPDATE: {response.get("message", "")}"
    assert response["data"] is not None, "UPDATE não retornou dados."
    assert len(response["data"]) == 1, "UPDATE retornou número inesperado de registros."
    assert response["data"][0]['capacity'] == updated_data['capacity'], "Dados atualizados não correspondem."
    print(f"✅ UPDATE OK | Capacidade: {response["data"][0]['capacity']}")

    # Limpeza específica para este teste
    try:
        supabase_client.from_(table_to_use).delete().eq("id", inserted_id).execute()
    except Exception as e:
        print(f"[WARNING] Falha na limpeza do UPDATE: {e}")

def test_supabase_crud_delete(supabase_client: Client, temp_table_name: str):
    """Testa a operação de DELETE via supabase_crud."""
    table_to_use = "recursos"
    test_data = {"name": f"Recurso Teste Delete {uuid.uuid4().hex[:4]}", "type": "sala", "capacity": 5, "location": "bloco D", "is_available": True}
    
    # Inserir um item para poder deletá-lo
    insert_response = supabase_crud(supabase_client, action="insert", table=table_to_use, data=test_data)
    assert insert_response["status"] == "success"
    inserted_id = insert_response["data"][0]['id']

    print(f"\n[INFO] Deletando dados de {table_to_use} com ID: {inserted_id}")
    response = supabase_crud(supabase_client, action="delete", table=table_to_use, query={"id": inserted_id})

    assert response["status"] == "success", f"Falha no DELETE: {response.get("message", "")}"
    assert response["data"] is not None, "DELETE não retornou dados."
    assert len(response["data"]) == 1, "DELETE retornou número inesperado de registros."
    print("✅ DELETE OK")

    # Verificar se o item foi realmente deletado
    check_response = supabase_crud(supabase_client, action="select", table=table_to_use, query={"id": inserted_id})
    assert check_response["status"] == "success"
    assert len(check_response["data"]) == 0, "Item não foi deletado corretamente."

