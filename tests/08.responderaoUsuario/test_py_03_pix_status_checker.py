import pytest
import os
from resipaia import update_pix_status, check_pix_status, get_supabase_client, SupabaseSchema
import uuid

@pytest.fixture(scope="module")
def supabase_client():
    if "SUPABASE_URL" not in os.environ or "SUPABASE_KEY" not in os.environ:
        pytest.skip("Variáveis de ambiente SUPABASE_URL e SUPABASE_KEY não configuradas para testes de integração.")
    
    client = get_supabase_client()
    yield client
    # Limpeza: Remover reservas de teste criadas por este módulo
    try:
        client.from_(SupabaseSchema.RESERVAS.name).delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    except Exception as e:
        print(f"Erro durante a limpeza do Supabase: {e}")

def generate_unique_txid():
    return str(uuid.uuid4())

def test_update_pix_status_success(supabase_client):
    txid = generate_unique_txid()
    # Inserir uma reserva com status pendente para ser atualizada
    supabase_client.from_(SupabaseSchema.RESERVAS.name).insert({
        "pix_txid": txid,
        "status": "pending",
        "user_id": str(uuid.uuid4()), # Adicionar user_id e resource_id
        "resource_id": str(uuid.uuid4()),
        "amount": 100.00,
        "start_time": "2025-07-20T10:00:00Z",
        "end_time": "2025-07-20T11:00:00Z"
    }).execute()

    message_details = {"txid": txid, "status": "paid"}
    response = update_pix_status(supabase_client, message_details)
    
    assert response["status"] == "success"
    assert "confirmado" in response["message"]
    
    # Verificar o status no banco de dados
    result = supabase_client.from_(SupabaseSchema.RESERVAS.name).select("status").eq("pix_txid", txid).single().execute()
    assert result.data["status"] == "paid"

def test_update_pix_status_no_reservation(supabase_client):
    txid = generate_unique_txid()
    message_details = {"txid": txid, "status": "paid"}
    
    response = update_pix_status(supabase_client, message_details)
    
    assert response["status"] == "error"
    assert "não encontrada" in response["message"]

def test_check_pix_status_paid(supabase_client):
    txid = generate_unique_txid()
    # Inserir uma reserva com status pago
    supabase_client.from_(SupabaseSchema.RESERVAS.name).insert({
        "pix_txid": txid,
        "status": "paid",
        "user_id": str(uuid.uuid4()),
        "resource_id": str(uuid.uuid4()),
        "amount": 200.00,
        "start_time": "2025-07-21T10:00:00Z",
        "end_time": "2025-07-21T11:00:00Z"
    }).execute()

    message_details = {"txid": txid}
    response = check_pix_status(supabase_client, message_details)
    
    assert response["status"] == "success"
    assert response["current_status"] == "paid"
    assert "está com status: paid" in response["message"]

def test_check_pix_status_pending(supabase_client):
    txid = generate_unique_txid()
    # Inserir uma reserva com status pendente
    supabase_client.from_(SupabaseSchema.RESERVAS.name).insert({
        "pix_txid": txid,
        "status": "pending",
        "user_id": str(uuid.uuid4()),
        "resource_id": str(uuid.uuid4()),
        "amount": 50.00,
        "start_time": "2025-07-22T10:00:00Z",
        "end_time": "2025-07-22T11:00:00Z"
    }).execute()

    message_details = {"txid": txid}
    response = check_pix_status(supabase_client, message_details)
    
    assert response["status"] == "success"
    assert response["current_status"] == "pending"
    assert "está com status: pending" in response["message"]

def test_check_pix_status_not_found(supabase_client):
    txid = generate_unique_txid()
    message_details = {"txid": txid}
    
    response = check_pix_status(supabase_client, message_details)
    
    assert response["status"] == "error"
    assert "não encontrada" in response["message"]

# Testes de exceção são mais complexos para simular com o cliente real
# e podem exigir mocks específicos para a camada de rede/DB.
# Por enquanto, vamos focar nos cenários de sucesso e falha de dados.
