import pytest
import json
from resipaia.interpretartexto.py_main_processor_v2 import process_message_logic

# Carrega os dados de teste do arquivo JSON
with open("C:\source\IAResipa\tests\06\interpretartexto\dados\test_data.json", 'r', encoding='utf-8') as f:
    test_data = json.load(f)

class TestNewUserRegistration:
    """
    Testes para validar o fluxo de registro de novo usuário.
    Baseado no cenário: 09.8.new_user_registration_flow_scenario.md
    """

    @pytest.fixture(scope="class")
    def setup_user_registration(self):
        """
        Pré-condições (Setup):
        - Sistema pronto para aceitar novos registros.
        - Dados de usuário válidos e inválidos para teste.
        """
        print("\nSetup: Configurando sistema para registro de novos usuários.")
        valid_user_data = test_data["test_03_new_user_registration"]["valid_user_data"]
        invalid_user_data = test_data["test_03_new_user_registration"]["invalid_user_data"]
        duplicate_email_data = test_data["test_03_new_user_registration"]["duplicate_email_data"]
        # Adicionar lógica para garantir que o sistema está pronto para registro
        yield {
            "valid_user_data": valid_user_data,
            "invalid_user_data": invalid_user_data,
            "duplicate_email_data": duplicate_email_data
        }
        print("Teardown: Removendo quaisquer usuários de teste criados.")
        # Adicionar lógica para remover usuários de teste

    def test_register_valid_user(self, setup_user_registration):
        """
        Cenário: Registrar_NovoUsuario (Usuário Válido)
        Objetivo: Validar que o registro com dados válidos é bem-sucedido e o usuário é criado no banco de dados.

        Ação Principal (Execute):
        - Usuário tenta se registrar com dados válidos.

        Validações (Assertions):
        - Confirmar que o registro com dados válidos é bem-sucedido e o usuário é criado no banco de dados.
        """
        test_case = test_data["test_03_new_user_registration"]["test_cases"][0]
        message_details = {
            "from": test_case["from"],
            "body": test_case["body_template"].format(valid_user_data=setup_user_registration['valid_user_data'])
        }
        response = process_message_logic(message_details)
        assert response["status"] in test_case["expected_status_options"]
        assert any(part in response["message"] for part in test_case["expected_message_parts"])

    def test_register_invalid_user(self, setup_user_registration):
        """
        Cenário: Registrar_NovoUsuario (Usuário Inválido)
        Objetivo: Validar que o registro com dados inválidos é rejeitado com mensagens de erro apropriadas.

        Ação Principal (Execute):
        - Usuário tenta se registrar com dados inválidos (ex: email duplicado, formato incorreto).

        Validações (Assertions):
        - Confirmar que o registro com dados inválidos é rejeitado com mensagens de erro apropriadas.
        """
        test_case = test_data["test_03_new_user_registration"]["test_cases"][1]
        message_details = {
            "from": test_case["from_template"].format(invalid_user_data=setup_user_registration['invalid_user_data']),
            "body": test_case["body_template"].format(invalid_user_data=setup_user_registration['invalid_user_data'])
        }
        response = process_message_logic(message_details)
        assert response["status"] == test_case["expected_status"]
        assert test_case["expected_message_part"] in response["message"]

    def test_register_duplicate_email(self, setup_user_registration):
        """
        Cenário: Registrar_NovoUsuario (Email Duplicado)
        Objetivo: Validar que o registro com email duplicado é rejeitado.

        Ação Principal (Execute):
        - Usuário tenta se registrar com email duplicado.

        Validações (Assertions):
        - Confirmar que o registro com email duplicado é rejeitado.
        """
        test_case = test_data["test_03_new_user_registration"]["test_cases"][2]
        # Primeiro, simular o registro do usuário válido para ter um email duplicado
        message_details_valid = {
            "from": test_case["from"],
            "body": test_case["body_template_valid"].format(valid_user_data=setup_user_registration['valid_user_data'])
        }
        process_message_logic(message_details_valid)

        message_details_duplicate = {
            "from": test_case["from"],
            "body": test_case["body_template_duplicate"].format(duplicate_email_data=setup_user_registration['duplicate_email_data'])
        }
        response = process_message_logic(message_details_duplicate)
        assert response["status"] == test_case["expected_status"]
        assert any(part in response["message"] for part in test_case["expected_message_part_options"])