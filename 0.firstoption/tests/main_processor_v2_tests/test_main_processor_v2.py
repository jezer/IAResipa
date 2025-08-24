import pytest
import json
import logging
import os
from datetime import datetime, timedelta # Adicionado para gerar timestamps únicos

# Importa a função a ser testada
from resipaia.interpretartexto.py_main_processor_v2 import process_message_logic

# Configuração de logging para os testes
# Garante que cada teste tenha seu próprio log
@pytest.fixture(autouse=True)
def setup_logging():
    log_dir = os.path.join(os.path.dirname(__file__), "test_results")
    os.makedirs(log_dir, exist_ok=True)
    
    # Cria um handler de arquivo para cada teste
    log_file = os.path.join(log_dir, f"test_log_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    
    # Adiciona o handler ao logger raiz
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    root_logger.setLevel(logging.INFO)
    
    yield # Permite que o teste seja executado
    
    # Remove o handler após o teste para evitar duplicação
    root_logger.removeHandler(file_handler)
    file_handler.close()


# Cenário 1: Usuário Não Cadastrado
def test_user_not_registered():
    unique_phone_number = f"5511999999999{datetime.now().strftime('%f')}"
    message_details = {
        "from": unique_phone_number + "@c.us",
        "body": "Olá",
        "type": "text"
    }
    response = process_message_logic(message_details)
    assert "Olá! Parece que você não está cadastrado. Por favor, faça seu cadastro para continuar." in response["message"]
    assert response["to"] == unique_phone_number
    logging.info(f"Teste 'Usuário Não Cadastrado' - Resposta: {response}")

# Cenário 2: Usuário Já Cadastrado
def test_user_already_registered():
    # Gera um número de telefone único para este teste
    unique_phone_number = f"5511999999999{datetime.now().strftime('%f')}"

    # Simula o registro do usuário
    register_message_details = {
        "from": unique_phone_number + "@c.us",
        "body": f"Cadastrar {unique_phone_number}",
        "type": "text"
    }
    process_message_logic(register_message_details) # Registra o usuário

    # Agora, testa a verificação do usuário já cadastrado
    message_details = {
        "from": unique_phone_number + "@c.us",
        "body": "Olá",
        "type": "text"
    }
    response = process_message_logic(message_details)
    assert f"Bem-vindo de volta, {unique_phone_number}! Como posso ajudar hoje?" in response["message"]
    assert response["to"] == unique_phone_number
    logging.info(f"Teste 'Usuário Já Cadastrado' - Resposta: {response}")

# Cenário 3: Administrador Cadastra Novo Usuário (Sucesso)
def test_admin_registers_new_user_success():
    message_details = {
        "from": "5511888888888@c.us", # Admin
        "body": f"Cadastrar 5511777777777{datetime.now().strftime('%f')}",
        "type": "text"
    }
    response = process_message_logic(message_details)
    assert "cadastrado com sucesso!" in response["message"]
    assert response["to"] == "5511888888888"
    logging.info(f"Teste 'Admin Cadastra Novo Usuário (Sucesso)' - Resposta: {response}")

# Cenário 4: Administrador Tenta Cadastrar com Número Inválido
def test_admin_registers_invalid_number():
    message_details = {
        "from": "5511888888888@c.us", # Admin
        "body": "Cadastrar abc",
        "type": "text"
    }
    response = process_message_logic(message_details)
    assert "Número de telefone inválido para cadastro. Por favor, forneça um número válido." in response["message"]
    assert response["to"] == "5511888888888"
    logging.info(f"Teste 'Admin Cadastra com Número Inválido' - Resposta: {response}")

# Cenário 5: Usuário Comum Tenta Cadastrar Novo Usuário
def test_common_user_registers_new_user():
    message_details = {
        "from": "5511999999999@c.us", # Usuário comum
        "body": f"Cadastrar 5511666666666{datetime.now().strftime('%f')}",
        "type": "text"
    }
    response = process_message_logic(message_details)
    assert "cadastrado com sucesso!" in response["message"]
    assert response["to"] == "5511999999999"
    logging.info(f"Teste 'Usuário Comum Tenta Cadastrar' - Resposta: {response}")

# Cenário para testar o envio de imagem
def test_send_image_message():
    message_details = {
        "from": "5511964703712@c.us",
        "body": "imagem 10",
        "type": "text"
    }
    response = process_message_logic(message_details)
    assert response["to"] == "5511964703712"
    assert "file" in response
    assert response["file"]["type"] == "image/jpeg"
    assert response["file"]["filename"] == "waha.jpg"
    assert "caption" in response
    logging.info(f"Teste 'Envio de Imagem' - Resposta: {response}")

# Cenário para testar a verificação de reservas ativas (sem reservas)
def test_check_active_reservations_no_reservations():
    message_details = {
        "from": "5511999999999@c.us",
        "body": "minhas reservas",
        "type": "text"
    }
    response = process_message_logic(message_details)
    assert "Você não possui reservas ativas no momento." in response["message"]
    assert response["to"] == "5511999999999"
    logging.info(f"Teste 'Verificar Reservas Ativas (sem reservas)' - Resposta: {response}")

# Cenário para testar a verificação de disponibilidade (sem recursos disponíveis)
def test_check_availability_no_resources():
    message_details = {
        "from": "5511999999999@c.us",
        "body": "opções disponíveis",
        "type": "text"
    }
    response = process_message_logic(message_details)
    assert "Nenhum recurso disponível no momento." in response["message"]
    assert response["to"] == "5511999999999"
    logging.info(f"Teste 'Verificar Disponibilidade (sem recursos)' - Resposta: {response}")

# Cenário para testar a criação de reserva provisória (sucesso)
def test_create_provisional_reservation_success():
    message_details = {
        "from": "5511999999999@c.us",
        "body": "reservar quiosque A",
        "type": "text"
    }
    response = process_message_logic(message_details)
    assert "Sua reserva provisória foi criada com sucesso!" in response["message"]
    assert response["to"] == "5511999999999"
    logging.info(f"Teste 'Criar Reserva Provisória (sucesso)' - Resposta: {response}")

# Cenário para testar a adição à lista de espera (sucesso)
def test_add_to_waiting_list_success():
    message_details = {
        "from": "5511999999999@c.us",
        "body": "entrar em lista de espera para quiosque B",
        "type": "text"
    }
    response = process_message_logic(message_details)
    assert "Você foi adicionado à lista de espera." in response["message"]
    assert response["to"] == "5511999999999"
    logging.info(f"Teste 'Adicionar à Lista de Espera (sucesso)' - Resposta: {response}")

# Cenário para testar mensagem de reserva não entendida
def test_unrecognized_reservation_message():
    message_details = {
        "from": "5511999999999@c.us",
        "body": "quero agendar",
        "type": "text"
    }
    response = process_message_logic(message_details)
    assert "Não entendi sua solicitação de reserva. Por favor, tente novamente com mais detalhes." in response["message"]
    assert response["to"] == "5511999999999"
    logging.info(f"Teste 'Mensagem de Reserva Não Entendida' - Resposta: {response}")

# Cenário para testar a remoção de usuário por um administrador
def test_admin_removes_user():
    # 1. Registrar um usuário para ser removido
    user_to_remove_phone = f"5511555555555{datetime.now().strftime('%f')}"
    register_message_details = {
        "from": user_to_remove_phone + "@c.us",
        "body": f"Cadastrar {user_to_remove_phone}",
        "type": "text"
    }
    process_message_logic(register_message_details)

    # 2. Simular a mensagem de remoção pelo admin
    admin_message_details = {
        "from": "5511888888888@c.us", # Admin
        "body": f"Remover usuario {user_to_remove_phone}",
        "type": "text"
    }
    response = process_message_logic(admin_message_details)
    assert f"Usuário {user_to_remove_phone} removido com sucesso!" in response["message"]
    assert response["to"] == "5511888888888"
    logging.info(f"Teste 'Admin Remove Usuário' - Resposta: {response}")
