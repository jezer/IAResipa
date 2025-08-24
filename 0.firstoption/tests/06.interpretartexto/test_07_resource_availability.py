import pytest
import json
from resipaia.interpretartexto.py_main_processor_v2 import process_message_logic

# Carrega os dados de teste do arquivo JSON
with open("C:\source\IAResipa\tests\06\interpretartexto\dados\test_data.json", 'r', encoding='utf-8') as f:
    test_data = json.load(f)

class TestResourceAvailability:
    """
    Testes para validar a verificação e seleção de disponibilidade de recursos.
    Baseado no cenário: 09.2.resource_availability_and_selection_scenario.md
    """

    @pytest.fixture(scope="class")
    def setup_resource_availability(self):
        """
        Pré-condições (Setup):
        - Base de dados de recursos com diferentes status de disponibilidade (disponível, ocupado, agendado).
        - Usuário autenticado no sistema.
        """
        print("""Setup: Configurando base de dados de recursos e autenticando usuário.""")
        # Simular criação de recursos com diferentes status no DB
        available_resource_id = test_data["test_07_resource_availability"]["available_resource_id"]
        unavailable_resource_id = test_data["test_07_resource_availability"]["unavailable_resource_id"]
        authenticated_user_id = test_data["test_07_resource_availability"]["authenticated_user_id"]
        yield {
            "available_resource_id": available_resource_id,
            "unavailable_resource_id": unavailable_resource_id,
            "authenticated_user_id": authenticated_user_id
        }
        print("Teardown: Revertendo o status de quaisquer recursos alterados.")
        # Adicionar lógica para reverter status de recursos

    def test_request_available_resource(self, setup_resource_availability):
        """
        Cenário: Verificar_Selecionar_Recurso (Recurso Disponível)
        Objetivo: Validar que o sistema retorna corretamente a disponibilidade de um recurso disponível.

        Ação Principal (Execute):
        - Usuário solicita a disponibilidade de um recurso em uma data/hora específica.
        - Usuário tenta selecionar um recurso disponível.

        Validações (Assertions):
        - Confirmar que o sistema retorna corretamente a disponibilidade dos recursos.
        - Confirmar que a seleção de um recurso disponível é bem-sucedida e o status do recurso é atualizado.
        """
        test_case = test_data["test_07_resource_availability"]["test_cases"][0]
        message_details = {
            "from": setup_resource_availability['authenticated_user_id'],
            "body": test_case["body_template"].format(available_resource_id=setup_resource_availability['available_resource_id'])
        }
        response = process_message_logic(message_details)
        assert response["status"] == test_case["expected_status"]
        assert test_case["expected_message_part"] in response["message"]

    def test_request_unavailable_resource(self, setup_resource_availability):
        """
        Cenário: Verificar_Selecionar_Recurso (Recurso Indisponível)
        Objetivo: Validar que a seleção de um recurso indisponível é rejeitada com uma mensagem apropriada.

        Ação Principal (Execute):
        - Usuário solicita a disponibilidade de um recurso em uma data/hora específica.
        - Usuário tenta selecionar um recurso indisponível.

        Validações (Assertions):
        - Confirmar que a seleção de um recurso indisponível é rejeitada com uma mensagem apropriada.
        """
        test_case = test_data["test_07_resource_availability"]["test_cases"][1]
        message_details = {
            "from": setup_resource_availability['authenticated_user_id'],
            "body": test_case["body_template"].format(unavailable_resource_id=setup_resource_availability['unavailable_resource_id'])
        }
        response = process_message_logic(message_details)
        assert response["status"] == test_case["expected_status"]
        assert test_case["expected_message_part"] in response["message"]