import pytest
import json
from unittest.mock import patch, MagicMock
import sys
import os

# Adiciona o diretório pai ao sys.path para permitir importações relativas


from resipaia import main, query_gemini, supabase_crud

@pytest.fixture
def mock_sys_argv():
    original_argv = sys.argv
    sys.argv = [original_argv[0]] # Reset argv para cada teste
    yield sys.argv
    sys.argv = original_argv # Restaurar argv

@pytest.fixture
def mock_print():
    with patch('builtins.print') as mock_print_func:
        yield mock_print_func

def create_message_details(phone_number, text_body, session="mock_session", push_name="MockUser", chat="mock_chat_id", msg_id="mock_msg_id", event="message", from_me=False, **kwargs):
    details = {
        "session": session,
        "PushName": push_name,
        "Chat": chat,
        "id": msg_id,
        "event": event,
        "fromMe": from_me,
        "text": {"body": text_body},
        "body": text_body,
        "from": phone_number
    }
    details.update(kwargs) # Adiciona quaisquer outros argumentos passados
    return details

@pytest.fixture
def mock_supabase_client():
    return MagicMock()

def test_query_gemini_hello():
    message_details = create_message_details("123", "Olá")
    result = query_gemini(message_details)
    assert result["status"] == "success"
    assert "Como posso ajudar" in result["response"]

def test_query_gemini_availability():
    message_details = create_message_details("123", "Quero saber a disponibilidade")
    result = query_gemini(message_details)
    assert result["status"] == "success"
    assert "preciso saber o tipo de recurso" in result["response"]

def test_query_gemini_other():
    message_details = create_message_details("123", "Qual a previsão do tempo?")
    result = query_gemini(message_details)
    assert result["status"] == "success"
    assert "estou focado em reservas e pagamentos" in result["response"]

def test_supabase_crud_insert(mock_supabase_client):
    data = {"name": "Test", "value": 1}
    mock_supabase_client.table.return_value.insert.return_value.execute.return_value.data = [{'id': 'test_id'}]
    result = supabase_crud(mock_supabase_client, "insert", "test_table", data=data)
    assert result["status"] == "success"
    assert "test_id" in result["data"][0]['id']

def test_supabase_crud_select(mock_supabase_client):
    mock_supabase_client.table.return_value.select.return_value.execute.return_value.data = [{'id': 'test_id', 'name': 'Test'}]
    result = supabase_crud(mock_supabase_client, "select", "test_table")
    assert result["status"] == "success"
    assert len(result["data"]) > 0

def test_supabase_crud_update(mock_supabase_client):
    data = {"value": 2}
    query = {"id": 1}
    mock_supabase_client.table.return_value.update.return_value.eq.return_value.execute.return_value.data = [{'id': 1, 'value': 2}]
    result = supabase_crud(mock_supabase_client, "update", "test_table", data=data, query=query)
    assert result["status"] == "success"
    assert result["data"][0]['value'] == 2

def test_supabase_crud_delete(mock_supabase_client):
    query = {"id": 1}
    mock_supabase_client.table.return_value.delete.return_value.eq.return_value.execute.return_value.data = [{'id': 1}]
    result = supabase_crud(mock_supabase_client, "delete", "test_table", query=query)
    assert result["status"] == "success"
    assert len(result["data"]) == 1

def test_supabase_crud_invalid_action(mock_supabase_client):
    result = supabase_crud(mock_supabase_client, "invalid_action", "test_table")
    assert result["status"] == "error"
    assert "Ação Supabase inválida" in result["message"]

def test_main_query_gemini(mock_sys_argv, mock_print):
    message_details = create_message_details("123", "Olá Gemini")
    mock_sys_argv.extend(["--query-gemini", json.dumps(message_details)])
    main()
    mock_print.assert_called_once()
    response = json.loads(mock_print.call_args[0][0])
    assert response["status"] == "success"
    assert "Como posso ajudar" in response["response"]

def test_main_supabase_crud_insert(mock_sys_argv, mock_print):
    data = {"name": "Test Resource", "type": "test", "capacity": 1}
    mock_sys_argv.extend(["--supabase-crud", "insert", "recursos", json.dumps(data)])
    main()
    mock_print.assert_called_once()
    response = json.loads(mock_print.call_args[0][0])
    assert response["status"] == "success"
    assert response["data"] is not None

def test_main_invalid_json(mock_sys_argv, mock_print):
    mock_sys_argv.extend(["--query-gemini", "invalid json"]) # Invalid JSON
    main()
    mock_print.assert_called_once()
    response = json.loads(mock_print.call_args[0][0])
    assert response["status"] == "error"
    assert "Detalhes da mensagem inválidos (JSON)" in response["message"]