import pytest
import os
from resipaia import generate_pix, get_supabase_client, SupabaseSchema
from datetime import datetime
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

def generate_unique_reservation_id():
    return str(uuid.uuid4())

def test_generate_pix_basic(supabase_client):
    reservation_id = generate_unique_reservation_id()
    message_details = {
        "amount": 100.50,
        "description": "Reserva de Quadra",
        "reservation_id": reservation_id
    }
    
    response = generate_pix(supabase_client, message_details)
    
    assert response["status"] == "success"
    assert reservation_id in response["txid"]
    assert "https://example.com/qrcode/" in response["qr_code_url"]
    assert "https://example.com/pix/" in response["pix_link"]
    assert "Pix gerado com sucesso! Valor: R$100.50." in response["message"]

def test_generate_pix_no_amount(supabase_client):
    reservation_id = generate_unique_reservation_id()
    message_details = {
        "description": "Reserva de Quiosque",
        "reservation_id": reservation_id
    }
    
    response = generate_pix(supabase_client, message_details)
    
    assert response["status"] == "success"
    assert reservation_id in response["txid"]
    assert "R$0.00" in response["message"]

def test_generate_pix_no_reservation_id(supabase_client):
    message_details = {
        "amount": 50.00,
        "description": "Pagamento"
    }
    
    response = generate_pix(supabase_client, message_details)
    
    assert response["status"] == "success"
    assert "TXID_GENERIC" in response["txid"]
    assert "R$50.00" in response["message"]
