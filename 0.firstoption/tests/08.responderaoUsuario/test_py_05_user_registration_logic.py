import pytest
import uuid
from resipaia import get_supabase_client, check_user, register_user
from datetime import datetime
import os
from resipaia.A_db.db_00_supabase_schema_config import SupabaseSchema

@pytest.fixture(scope="module")
def supabase_client():
    # Verifica se as variáveis de ambiente estão configuradas
    if "SUPABASE_URL" not in os.environ or "SUPABASE_KEY" not in os.environ:
        pytest.skip("Variáveis de ambiente SUPABASE_URL e SUPABASE_KEY não configuradas para testes de integração.")
    
    client = get_supabase_client()
    yield client

def generate_unique_phone_number():
    # Gera um número de telefone único para cada execução de teste
    return f"+551199999{uuid.uuid4().hex[:6]}"

def test_check_user_found(supabase_client, supabase_test_user):
    # Primeiro, registra um usuário para garantir que ele exista
    unique_phone = supabase_test_user
    message_details_check = {"from": unique_phone}
    response = check_user(supabase_client, message_details_check)
    
    assert response["status"] == "user_found"
    assert "Bem-vindo de volta" in response["message"]

def test_check_user_not_found(supabase_client):
    unique_phone = generate_unique_phone_number()
    message_details = {"from": unique_phone}
    
    response = check_user(supabase_client, message_details)
    
    assert response["status"] == "user_not_found"
    assert "não está cadastrado" in response["message"]

def test_register_user_success(supabase_client):
    unique_phone = generate_unique_phone_number()
    message_details = {"from": unique_phone, "name": "Teste User"}
    
    response = register_user(supabase_client, message_details)
    
    assert response["status"] == "registration_success"
    assert "cadastrado com sucesso" in response["message"]

    # Cleanup: Remove the newly registered user
    supabase_client.from_(SupabaseSchema.CADASTRO_PESSOAS_FISICA.name).delete().eq("phone_number", unique_phone).execute()

def test_register_user_failure(supabase_client):
    # Exemplo: Tentar registrar um usuário com um número de telefone que já existe
    unique_phone = generate_unique_phone_number()
    message_details_first_register = {"from": unique_phone, "name": "First User"}
    register_user(supabase_client, message_details_first_register) # Registra o primeiro usuário

    message_details_second_register = {"from": unique_phone, "name": "Second User"}
    response = register_user(supabase_client, message_details_second_register) # Tenta registrar o mesmo número novamente
    
    assert response["status"] == "error"
    assert "Erro ao registrar usuário" in response["message"] or "duplicate key value violates unique constraint" in response["message"]

    # Cleanup: Remove the registered user
    supabase_client.from_(SupabaseSchema.CADASTRO_PESSOAS_FISICA.name).delete().eq("phone_number", unique_phone).execute()
