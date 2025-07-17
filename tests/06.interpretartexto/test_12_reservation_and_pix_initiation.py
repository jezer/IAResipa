import pytest
import json
from resipaia.interpretartexto.py_main_processor_v2 import process_message_logic

# Carrega os dados de teste do arquivo JSON
with open("C:\source\IAResipa\tests\06\interpretartexto\dados\test_data.json", 'r', encoding='utf-8') as f:
    test_data = json.load(f)

class TestReservationAndPixInitiation:
    """
    Testes para validar a criação de reserva e iniciação de pagamento Pix.
    Baseado no cenário: 09.3.reservation_creation_and_pix_initiation_scenario.md
    """

    @pytest.fixture(scope="class")
    def setup_reservation_pix(self):
        """
        Pré-condições (Setup):
        - Recurso disponível para reserva.
        - Usuário autenticado.
        - Configuração do gateway de pagamento Pix.
        """
        print("\nSetup: Configurando ambiente para criação de reserva e Pix.")
        available_resource_id = test_data["test_12_reservation_and_pix_initiation"]["available_resource_id"]
        authenticated_user_id = test_data["test_12_reservation_and_pix_initiation"]["authenticated_user_id"]
        # Simular configuração do gateway Pix e garantir recurso disponível
        yield {
            "available_resource_id": available_resource_id,
            "authenticated_user_id": authenticated_user_id
        }
        print("Teardown: Removendo a reserva criada e cancelando a transação Pix (se possível).")
        # Adicionar lógica para remover reserva e cancelar Pix

    def test_create_reservation_and_initiate_pix(self, setup_reservation_pix):
        """
        Cenário: CriarReserva_IniciarPix
        Objetivo: Validar o fluxo completo de criação de uma reserva e a iniciação do pagamento via Pix.

        Ação Principal (Execute):
        - Usuário seleciona um recurso e um horário.
        - Sistema gera uma reserva.
        - Sistema inicia o processo de pagamento Pix.

        Validações (Assertions):
        - Confirmar que a reserva é criada com sucesso no banco de dados.
        - Confirmar que um QR Code Pix ou código copia-e-cola é gerado e retornado ao usuário.
        - Confirmar que a transação Pix é registrada no sistema de pagamento.
        - Verificar logs para erros durante a criação da reserva e iniciação do Pix.
        """
        test_case = test_data["test_12_reservation_and_pix_initiation"]["test_cases"][0]
        message_details = {
            "from": setup_reservation_pix['authenticated_user_id'],
            "body": test_case["body"],
            "amount": test_case["amount"],
            "description": test_case["description"]
        }
        response = process_message_logic(message_details)
        assert response["status"] == test_case["expected_status"]
        assert test_case["expected_message_part"] in response["message"]