import pytest
import json
from resipaia.interpretartexto.py_main_processor_v2 import process_message_logic

# Carrega os dados de teste do arquivo JSON
with open("C:\\source\\IAResipa\\tests\\06\\interpretartexto\\dados\\test_data.json", 'r', encoding='utf-8') as f:
    test_data = json.load(f)

class TestWhatsappMessageReception:
    """
    Testes para validar a recepção de mensagens do WhatsApp e verificação de usuário.
    Baseado no cenário: 09.1.whatsapp_message_reception_and_user_check_scenario.md
    """

    @pytest.fixture(scope="class")
    def setup_whatsapp_reception(self):
        """
        Pré-condições (Setup):
        - Sistema configurado para receber mensagens do WhatsApp (Webhook ativo).
        - Base de dados de usuários acessível.
        - Usuário de teste pré-cadastrado e não cadastrado.
        """
        print("""Setup: Configurando ambiente para recepção de mensagens WhatsApp.""")
        # Simular configuração de webhook, acesso ao DB, criação de usuários de teste
        registered_user_number = test_data["test_09_whatsapp_message_reception"]["registered_user_number"]
        unregistered_user_number = test_data["test_09_whatsapp_message_reception"]["unregistered_user_number"]
        yield {
            "registered_user_number": registered_user_number,
            "unregistered_user_number": unregistered_user_number
        }
        print("Teardown: Removendo dados de teste gerados.")
        # Adicionar lógica para remover mensagens, registros temporários, etc.

    def test_receive_message_from_registered_user(self, setup_whatsapp_reception):
        """
        Cenário: ReceberMensagem_VerificarUsuario (Usuário Cadastrado)
        Objetivo: Validar que a mensagem de um usuário cadastrado é processada e o usuário é identificado corretamente.

        Ação Principal (Execute):
        - Enviar uma mensagem de um número de WhatsApp cadastrado.

        Validações (Assertions):
        - Confirmar que a mensagem do usuário cadastrado é processada e o usuário é identificado corretamente.
        - Verificar logs para erros durante a recepção e verificação.
        """
        test_case = test_data["test_09_whatsapp_message_reception"]["test_cases"][0]
        message_details = {
            "from": setup_whatsapp_reception['registered_user_number'],
            "body": test_case["body"]
        }
        response = process_message_logic(message_details)
        assert response["to"] == setup_whatsapp_reception['registered_user_number']
        assert test_case["expected_message_part"] in response["message"]

    def test_receive_message_from_unregistered_user(self, setup_whatsapp_reception):
        """
        Cenário: ReceberMensagem_VerificarUsuario (Usuário Não Cadastrado)
        Objetivo: Validar que a mensagem de um usuário não cadastrado aciona o fluxo de registro de novo usuário.

        Ação Principal (Execute):
        - Enviar uma mensagem de um número de WhatsApp não cadastrado.

        Validações (Assertions):
        - Confirmar que a mensagem do usuário não cadastrado aciona o fluxo de registro de novo usuário.
        - Verificar logs para erros durante a recepção e verificação.
        """
        test_case = test_data["test_09_whatsapp_message_reception"]["test_cases"][1]
        message_details = {
            "from": setup_whatsapp_reception['unregistered_user_number'],
            "body": test_case["body"]
        }
        response = process_message_logic(message_details)
        assert response["to"] == setup_whatsapp_reception['unregistered_user_number']
        assert test_case["expected_message_part"] in response["message"]