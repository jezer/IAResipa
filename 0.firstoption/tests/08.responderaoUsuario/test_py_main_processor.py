import pytest

import resipaia
from resipaia import process_message

@pytest.fixture
def mock_message_details():
    return {
        "from": "123456789@c.us",
        "body": "Olá",
        "text": "Olá"
    }

def test_process_message_ola(mocker, mock_message_details):
    mock_handle_user_check = mocker.patch('resipaia.codbackup.py_main_processor.handle_user_check', return_value={"to": "123456789", "message": "Verificação de usuário em andamento."})
    
    message_details = mock_message_details
    message_details["body"] = "olá"
    message_details["text"] = "olá"

    response = process_message(message_details)
    
    mock_handle_user_check.assert_called_once_with({"from": "123456789", "body": "olá", "text": "olá"})
    assert response == {"to": "123456789", "message": "Verificação de usuário em andamento."}

def test_process_message_reservar(mocker, mock_message_details):
    mock_handle_reservation = mocker.patch('resipaia.codbackup.py_main_processor.handle_reservation', return_value={"to": "123456789", "message": "Processando sua solicitação de reserva."})
    
    message_details = mock_message_details
    message_details["body"] = "quero reservar"
    message_details["text"] = "quero reservar"

    response = process_message(message_details)
    
    mock_handle_reservation.assert_called_once_with({"from": "123456789", "body": "quero reservar", "text": "quero reservar"})
    assert response == {"to": "123456789", "message": "Processando sua solicitação de reserva."}

def test_process_message_pix(mocker, mock_message_details):
    mock_handle_pix_initiation = mocker.patch('resipaia.codbackup.py_main_processor.handle_pix_initiation', return_value={"to": "123456789", "message": "Iniciando processo Pix."})
    
    message_details = mock_message_details
    message_details["body"] = "fazer pix"
    message_details["text"] = "fazer pix"

    response = process_message(message_details)
    
    mock_handle_pix_initiation.assert_called_once_with({"from": "123456789", "body": "fazer pix", "text": "fazer pix"})
    assert response == {"to": "123456789", "message": "Iniciando processo Pix."}

def test_process_message_status_pix(mocker, mock_message_details):
    mock_handle_pix_status_check = mocker.patch('resipaia.codbackup.py_main_processor.handle_pix_status_check', return_value={"to": "123456789", "message": "Verificando status Pix."})
    
    message_details = mock_message_details
    message_details["body"] = "status pix"
    message_details["text"] = "status pix"

    response = process_message(message_details)
    
    mock_handle_pix_status_check.assert_called_once_with({"from": "123456789", "body": "status pix", "text": "status pix"})
    assert response == {"to": "123456789", "message": "Verificando status Pix."}

def test_process_message_cancelar(mocker, mock_message_details):
    mock_handle_cancellation = mocker.patch('resipaia.codbackup.py_main_processor.handle_cancellation', return_value={"to": "123456789", "message": "Processando seu cancelamento."})
    
    message_details = mock_message_details
    message_details["body"] = "cancelar reserva"
    message_details["text"] = "cancelar reserva"

    response = process_message(message_details)
    
    mock_handle_cancellation.assert_called_once_with({"from": "123456789", "body": "cancelar reserva", "text": "cancelar reserva"})
    assert response == {"to": "123456789", "message": "Processando seu cancelamento."}

def test_process_message_gerenciar_reservas(mocker, mock_message_details):
    mock_handle_manage_reservations = mocker.patch('resipaia.codbackup.py_main_processor.handle_manage_reservations', return_value={"to": "123456789", "message": "Gerenciando suas reservas."})
    
    message_details = mock_message_details
    message_details["body"] = "minhas reservas"
    message_details["text"] = "minhas reservas"

    response = process_message(message_details)
    
    mock_handle_manage_reservations.assert_called_once_with({"from": "123456789", "body": "minhas reservas", "text": "minhas reservas"})
    assert response == {"to": "123456789", "message": "Gerenciando suas reservas."}

def test_process_message_cadastrar(mocker, mock_message_details):
    mock_handle_user_check = mocker.patch('resipaia.codbackup.py_main_processor.handle_user_check', return_value={"to": "123456789", "message": "Verificação de usuário em andamento."})
    
    message_details = mock_message_details
    message_details["body"] = "cadastrar"
    message_details["text"] = "cadastrar"

    response = process_message(message_details)
    
    mock_handle_user_check.assert_called_once_with({"from": "123456789", "body": "cadastrar", "text": "cadastrar"})
    assert response == {"to": "123456789", "message": "Verificação de usuário em andamento."}

def test_process_message_gemini_fallback(mocker, mock_message_details):
    mock_handle_gemini_query = mocker.patch('resipaia.codbackup.py_main_processor.handle_gemini_query', return_value={"to": "123456789", "message": "Consultando Gemini."})
    
    message_details = mock_message_details
    message_details["body"] = "alguma outra coisa"
    message_details["text"] = "alguma outra coisa"

    response = process_message(message_details)
    
    mock_handle_gemini_query.assert_called_once_with({"from": "123456789", "body": "alguma outra coisa", "text": "alguma outra coisa"})
    assert response == {"to": "123456789", "message": "Consultando Gemini."}

def test_process_message_no_from_number(mocker, mock_message_details):
    message_details = mock_message_details
    message_details["from"] = ""
    message_details["body"] = "olá"
    message_details["text"] = "olá"

    response = process_message(message_details)
    
    assert response == {"to": "error", "message": "Número de telefone do remetente não encontrado."}
    mock_handle_user_check = mocker.patch('resipaia.codbackup.py_main_processor.handle_user_check')
    mock_handle_reservation = mocker.patch('resipaia.codbackup.py_main_processor.handle_reservation')
    mock_handle_pix_initiation = mocker.patch('resipaia.codbackup.py_main_processor.handle_pix_initiation')
    mock_handle_pix_status_check = mocker.patch('resipaia.codbackup.py_main_processor.handle_pix_status_check')
    mock_handle_cancellation = mocker.patch('resipaia.codbackup.py_main_processor.handle_cancellation')
    mock_handle_manage_reservations = mocker.patch('resipaia.codbackup.py_main_processor.handle_manage_reservations')
    mock_handle_gemini_query = mocker.patch('resipaia.codbackup.py_main_processor.handle_gemini_query')
    mock_handle_user_check.assert_not_called()
    mock_handle_reservation.assert_not_called()
    mock_handle_pix_initiation.assert_not_called()
    mock_handle_pix_status_check.assert_not_called()
    mock_handle_cancellation.assert_not_called()
    mock_handle_manage_reservations.assert_not_called()
    mock_handle_gemini_query.assert_not_called()

def test_process_message_body_and_text_handling(mocker, mock_message_details):
    mock_handle_user_check = mocker.patch('resipaia.codbackup.py_main_processor.handle_user_check', return_value={"to": "123456789", "message": "Verificação de usuário em andamento."})
    
    message_details = {"from": "123456789@c.us", "body": "", "text": "olá"}
    response = process_message(message_details)
    assert message_details["body"] == "olá"
    assert message_details["text"] == "olá"
    mock_handle_user_check.assert_called_once_with({"from": "123456789", "body": "olá", "text": "olá"})

    message_details = {"from": "123456789@c.us", "body": "oi", "text": ""}
    response = process_message(message_details)
    assert message_details["body"] == "oi"
    assert message_details["text"] == "oi"
    mock_handle_user_check.assert_called_with({"from": "123456789", "body": "oi", "text": "oi"})

    message_details = {"from": "123456789@c.us", "body": "", "text": ""}
    response = process_message(message_details)
    assert message_details["body"] == ""
    assert message_details["text"] == ""
    mock_handle_gemini_query = mocker.patch('resipaia.codbackup.py_main_processor.handle_gemini_query')
    mock_handle_gemini_query.assert_called_once_with({"from": "123456789", "body": "", "text": ""})