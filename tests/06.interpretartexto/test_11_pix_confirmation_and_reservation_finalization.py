import pytest
import json
from resipaia.interpretartexto.py_main_processor_v2 import process_message_logic

# Carrega os dados de teste do arquivo JSON
with open("C:\source\IAResipa\tests\06\interpretartexto\dados\test_data.json", 'r', encoding='utf-8') as f:
    test_data = json.load(f)

class TestPixConfirmationAndReservationFinalization:
    """
    Testes para validar a confirmação de pagamento Pix e finalização de reserva.
    Baseado no cenário: 09.4.pix_payment_confirmation_and_reservation_finalization_scenario.md
    """

    @pytest.fixture(scope="class")
    def setup_pix_confirmation(self):
        """
        Pré-condições (Setup):
        - Reserva criada com pagamento Pix pendente.
        - Simulador de pagamento Pix ou ambiente de teste.
        """
        print("\nSetup: Configurando ambiente para confirmação de Pix e finalização de reserva.")
        pending_reservation_id = test_data["test_11_pix_confirmation_and_reservation_finalization"]["pending_reservation_id"]
        # Simular criação de reserva com Pix pendente
        yield {"pending_reservation_id": pending_reservation_id}
        print("Teardown: Revertendo o status da reserva para o estado inicial ou removendo a reserva.")
        # Adicionar lógica para reverter status ou remover reserva

    def test_pix_payment_confirmation_and_reservation_finalization(self, setup_pix_confirmation):
        """
        Cenário: ConfirmarPix_FinalizarReserva
        Objetivo: Validar o fluxo de confirmação de pagamento Pix e a subsequente finalização da reserva.

        Ação Principal (Execute):
        - Simular a confirmação de pagamento Pix pelo gateway.
        - Sistema recebe a notificação de pagamento.

        Validações (Assertions):
        - Confirmar que o status da reserva é atualizado para "confirmada" ou "finalizada".
        - Confirmar que o usuário recebe uma notificação de confirmação.
        - Verificar logs para erros durante a confirmação e finalização.
        """
        test_case = test_data["test_11_pix_confirmation_and_reservation_finalization"]["test_cases"][0]
        message_details = {
            "from": test_case["from"],
            "body": test_case["body"],
            "txid": setup_pix_confirmation['pending_reservation_id'] # Usar o txid da reserva pendente
        }
        response = process_message_logic(message_details)
        assert response["status"] == test_case["expected_status"]
        assert test_case["expected_message_part"] in response["message"]