import pytest
from unittest.mock import MagicMock, patch
from resipaia import check_user, register_user

@pytest.fixture
def mock_supabase_client():
    return MagicMock()

def test_check_user_found(mock_supabase_client):
    message_details = {"from": "+5511999998888"}
    mock_supabase_client.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value.data = {"id": "user_uuid", "phone_number": "+5511999998888"}
    
    response = check_user(mock_supabase_client, message_details)
    
    assert response["status"] == "user_found"
    assert "Bem-vindo de volta" in response["message"]
    mock_supabase_client.table.assert_called_with('cadastro_pessoas_fisica')
    mock_supabase_client.table.return_value.select.assert_called_with('id', 'phone_number')
    mock_supabase_client.table.return_value.select.return_value.eq.assert_called_with('phone_number', '+5511999998888')

def test_check_user_not_found(mock_supabase_client):
    message_details = {"from": "+5511999997777"}
    mock_supabase_client.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value.data = None
    
    response = check_user(mock_supabase_client, message_details)
    
    assert response["status"] == "user_not_found"
    assert "não está cadastrado" in response["message"]

def test_register_user_success(mock_supabase_client):
    message_details = {"from": "+5511999996666", "name": "Teste User"}
    mock_supabase_client.table.return_value.insert.return_value.execute.return_value.data = [{'id': 'new_user_uuid', 'phone_number': '+5511999996666'}]
    
    response = register_user(mock_supabase_client, message_details)
    
    assert response["status"] == "registration_success"
    assert "cadastrado com sucesso" in response["message"]
    mock_supabase_client.table.assert_called_with('cadastro_pessoas_fisica')
    mock_supabase_client.table.return_value.insert.assert_called_with({'phone_number': '+5511999996666', 'name': 'Teste User'})

def test_register_user_failure(mock_supabase_client):
    message_details = {"from": "+5511999995555", "name": "Fail User"}
    mock_supabase_client.table.return_value.insert.return_value.execute.side_effect = Exception("Erro de banco de dados")
    
    response = register_user(mock_supabase_client, message_details)
    
    assert response["status"] == "error"
    assert "Erro de banco de dados" in response["message"]
