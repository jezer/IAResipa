import pytest
import json
import os
from resipaia.interpretartexto.py_main_processor_v2 import process_message_logic

# Carrega os dados de teste do arquivo JSON
current_dir = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(current_dir, "dados", "test_data.json")
with open(data_file_path, 'r', encoding='utf-8') as f:
    test_data = json.load(f)

class TestExistingReservationManagement:
    """
    Testes para validar o gerenciamento de reservas existentes.
    Baseado no cenário: 09.7.existing_reservation_management_scenario.md
    """

    @pytest.fixture(scope="class")
    def setup_reservation_management(self):
        """
        Pré-condições (Setup):
        - Usuário com reservas ativas e passadas.
        """
        print("\nSetup: Configurando usuário com reservas ativas e passadas.")
        user_id = test_data["test_01_existing_reservation_management"]["user_id"]
        active_reservation_id = test_data["test_01_existing_reservation_management"]["active_reservation_id"]
        past_reservation_id = test_data["test_01_existing_reservation_management"]["past_reservation_id"]
        # Simular criação de reservas para o usuário
        yield {
            "user_id": user_id,
            "active_reservation_id": active_reservation_id,
            "past_reservation_id": past_reservation_id
        }
        print("Teardown: Reverter quaisquer modificações ou remover reservas de teste.")
        # Adicionar lógica para limpeza

    def test_view_all_reservations(self, setup_reservation_management):
        """
        Cenário: Gerenciar_ReservasExistentes (Visualização)
        Objetivo: Validar que o usuário consegue visualizar todas as suas reservas.

        Ação Principal (Execute):
        - Usuário solicita a visualização de suas reservas.

        Validações (Assertions):
        - Confirmar que o usuário consegue visualizar todas as suas reservas.
        """
        test_case = test_data["test_01_existing_reservation_management"]["test_cases"][0]
        message_details = {
            "from": setup_reservation_management['user_id'],
            "body": test_case["body"]
        }
        response = process_message_logic(message_details)
        assert response["status"] == test_case["expected_status"]
        assert test_case["expected_reservations_in_response"] == ("reservations" in response)

    def test_modify_reservation(self, setup_reservation_management):
        """
        Cenário: Gerenciar_ReservasExistentes (Modificação)
        Objetivo: Validar que as modificações são aplicadas corretamente e refletidas no sistema.

        Ação Principal (Execute):
        - Usuário tenta modificar uma reserva (data, hora, recurso).

        Validações (Assertions):
        - Confirmar que as modificações são aplicadas corretamente e refletidas no sistema.
        """
        test_case = test_data["test_01_existing_reservation_management"]["test_cases"][1]
        message_details = {
            "from": setup_reservation_management['user_id'],
            "body": test_case["body_template"].format(active_reservation_id=setup_reservation_management['active_reservation_id'])
        }
        response = process_message_logic(message_details)
        assert response["status"] == test_case["expected_status"]

    def test_cancel_reservation(self, setup_reservation_management):
        """
        Cenário: Gerenciar_ReservasExistentes (Cancelamento)
        Objetivo: Validar que o cancelamento de reserva é processado e o status é atualizado.

        Ação Principal (Execute):
        - Usuário tenta cancelar uma reserva.

        Validações (Assertions):
        - Confirmar que o cancelamento de reserva é processado e o status é atualizado.
        """
        test_case = test_data["test_01_existing_reservation_management"]["test_cases"][2]
        message_details = {
            "from": setup_reservation_management['user_id'],
            "body": test_case["body_template"].format(active_reservation_id=setup_reservation_management['active_reservation_id'])
        }
        response = process_message_logic(message_details)
        assert response["status"] == test_case["expected_status"]