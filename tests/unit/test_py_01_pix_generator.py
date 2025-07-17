import pytest
from unittest.mock import MagicMock
from resipaia import generate_pix

@pytest.fixture
def mock_supabase_client():
    return MagicMock()

def test_generate_pix_basic(mock_supabase_client):
    message_details = {
        "amount": 100.50,
        "description": "Reserva de Quadra",
        "reservation_id": "RES001"
    }
    
    response = generate_pix(mock_supabase_client, message_details)
    
    assert response["status"] == "success"
    assert "TXID_RES001_100.5" in response["txid"]
    assert "https://example.com/qrcode/TXID_RES001_100.5" in response["qr_code_url"]
    assert "https://example.com/pix/TXID_RES001_100.5" in response["pix_link"]
    assert "Pix gerado com sucesso! Valor: R$100.50. Escaneie o QR Code ou use o link: https://example.com/pix/TXID_RES001_100.5" in response["message"]

def test_generate_pix_no_amount(mock_supabase_client):
    message_details = {
        "description": "Reserva de Quiosque",
        "reservation_id": "RES002"
    }
    
    response = generate_pix(mock_supabase_client, message_details)
    
    assert response["status"] == "success"
    assert "TXID_RES002_0" in response["txid"]
    assert "R$0.00" in response["message"]

def test_generate_pix_no_reservation_id(mock_supabase_client):
    message_details = {
        "amount": 50.00,
        "description": "Pagamento"
    }
    
    response = generate_pix(mock_supabase_client, message_details)
    
    assert response["status"] == "success"
    assert "TXID_GENERIC_50" in response["txid"]
    assert "R$50.00" in response["message"]
