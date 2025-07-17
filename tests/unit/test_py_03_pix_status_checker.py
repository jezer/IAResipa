import pytest
from unittest.mock import MagicMock, patch
from resipaia import update_pix_status, check_pix_status

@pytest.fixture
def mock_supabase_client():
    return MagicMock()

def test_update_pix_status_success(mock_supabase_client):
    message_details = {"txid": "TXID123", "status": "paid"}
    
    # Mock do execute().data
    mock_supabase_client.table.return_value.update.return_value.eq.return_value.execute.return_value.data = [{'id': 'some_uuid', 'pix_txid': 'TXID123', 'status': 'paid'}]

    response = update_pix_status(mock_supabase_client, message_details)
    
    mock_supabase_client.table.assert_called_with('reservas')
    mock_supabase_client.table.return_value.update.assert_called_with({'status': 'paid'})
    mock_supabase_client.table.return_value.update.return_value.eq.assert_called_with('pix_txid', 'TXID123')
    mock_supabase_client.table.return_value.update.return_value.eq.return_value.execute.assert_called_once()
    
    assert response["status"] == "success"
    assert "confirmado" in response["message"]

def test_update_pix_status_no_reservation(mock_supabase_client):
    message_details = {"txid": "TXID456", "status": "paid"}
    
    # Mock do execute().data para retornar vazio (nenhuma reserva encontrada)
    mock_supabase_client.table.return_value.update.return_value.eq.return_value.execute.return_value.data = []

    response = update_pix_status(mock_supabase_client, message_details)
    
    assert response["status"] == "error"
    assert "não encontrada" in response["message"]

def test_update_pix_status_exception(mock_supabase_client):
    message_details = {"txid": "TXID789", "status": "paid"}
    
    # Simula uma exceção durante a execução
    mock_supabase_client.table.return_value.update.return_value.eq.return_value.execute.side_effect = Exception("Erro de conexão")

    response = update_pix_status(mock_supabase_client, message_details)
    
    assert response["status"] == "error"
    assert "Erro de conexão" in response["message"]

def test_check_pix_status_paid(mock_supabase_client):
    message_details = {"txid": "TXID101"}
    
    # Mock do execute().data para retornar status 'paid'
    mock_supabase_client.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value.data = {'status': 'paid'}

    response = check_pix_status(mock_supabase_client, message_details)
    
    mock_supabase_client.table.assert_called_with('reservas')
    mock_supabase_client.table.return_value.select.assert_called_with('status')
    mock_supabase_client.table.return_value.select.return_value.eq.assert_called_with('pix_txid', 'TXID101')
    mock_supabase_client.table.return_value.select.return_value.eq.return_value.single.assert_called_once()
    
    assert response["status"] == "success"
    assert response["current_status"] == "paid"
    assert "está com status: paid" in response["message"]

def test_check_pix_status_pending(mock_supabase_client):
    message_details = {"txid": "TXID102"}
    
    # Mock do execute().data para retornar status 'pending'
    mock_supabase_client.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value.data = {'status': 'pending'}

    response = check_pix_status(mock_supabase_client, message_details)
    
    assert response["status"] == "success"
    assert response["current_status"] == "pending"
    assert "está com status: pending" in response["message"]

def test_check_pix_status_not_found(mock_supabase_client):
    message_details = {"txid": "TXID103"}
    
    # Mock do execute().data para retornar None (reserva não encontrada)
    mock_supabase_client.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value.data = None

    response = check_pix_status(mock_supabase_client, message_details)
    
    assert response["status"] == "error"
    assert "não encontrada" in response["message"]

def test_check_pix_status_exception(mock_supabase_client):
    message_details = {"txid": "TXID104"}
    
    # Simula uma exceção durante a execução
    mock_supabase_client.table.return_value.select.return_value.eq.return_value.single.return_value.execute.side_effect = Exception("Erro de rede")

    response = check_pix_status(mock_supabase_client, message_details)
    
    assert response["status"] == "error"
    assert "Erro de rede" in response["message"]
