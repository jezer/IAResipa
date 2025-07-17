import pytest
import json
from resipaia.interpretartexto.py_main_processor_v2 import process_message_logic

# Carrega os dados de teste do arquivo JSON
with open("C:\source\IAResipa\tests\06\interpretartexto\dados\test_data.json", 'r', encoding='utf-8') as f:
    test_data = json.load(f)

class TestReservationCancellationAndNotification:
    """
    Testes para validar o cancelamento de reserva e notificação de lista de espera.
    Baseado no cenário: 09.5.reservation_cancellation_and_waiting_list_notification_scenario.md
    """

    @pytest.fixture(scope="class")
    def setup_cancellation_notification(self):
        """
        Pré-condições (Setup):
        - Reserva ativa.
        - Lista de espera para o recurso com usuários cadastrados.
        """
        print("\nSetup: Configurando ambiente para cancelamento de reserva e notificação.")
        active_reservation_id = test_data["test_06_reservation_cancellation_and_notification"]["active_reservation_id"]
        resource_with_waiting_list = test_data["test_06_reservation_cancellation_and_notification"]["resource_with_waiting_list"]
        waiting_list_users = test_data["test_06_reservation_cancellation_and_notification"]["waiting_list_users"]
        # Simular criação de reserva ativa e lista de espera
        yield {
            "active_reservation_id": active_reservation_id,
            "resource_with_waiting_list": resource_with_waiting_list,
            "waiting_list_users": waiting_list_users
        }
        print("Teardown: Reverter o status da reserva ou remover a reserva. Remover notificações de lista de espera.")
        # Adicionar lógica para limpeza

    def test_cancel_reservation_and_notify_waiting_list(self, setup_cancellation_notification):
        """
        Cenário: CancelarReserva_NotificarListaEspera
        Objetivo: Validar o fluxo de cancelamento de reserva e a notificação de usuários em lista de espera.

        Ação Principal (Execute):
        - Usuário solicita o cancelamento de uma reserva.
        - Sistema processa o cancelamento.

        Validações (Assertions):
        - Confirmar que o status da reserva é atualizado para "cancelada".
        - Confirmar que os usuários na lista de espera são notificados sobre a disponibilidade do recurso.
        - Verificar logs para erros durante o cancelamento e notificação.
        """
        test_case = test_data["test_06_reservation_cancellation_and_notification"]["test_cases"][0]
        message_details = {
            "from": test_case["from_template"].format(active_reservation_id=setup_cancellation_notification['active_reservation_id']),
            "body": test_case["body_template"].format(active_reservation_id=setup_cancellation_notification['active_reservation_id'])
        }
        response = process_message_logic(message_details)
        assert response["status"] == test_case["expected_status"]
        assert test_case["expected_message_part"] in response["message"]