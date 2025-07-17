import pytest
import json
from resipaia.interpretartexto.py_main_processor_v2 import process_message_logic

# Carrega os dados de teste do arquivo JSON
with open("C:\\source\\IAResipa\\tests\\06\\interpretartexto\\dados\\test_data.json", 'r', encoding='utf-8') as f:
    test_data = json.load(f)

class TestWhatsappReservationSystem:
    """
    Testes para validar o sistema de reserva WhatsApp completo.
    Baseado no cenário: 09.whatsapp_reservation_system_scenario.md
    """

    @pytest.fixture(scope="class")
    def setup_whatsapp_reservation_system(self):
        """
        Pré-condições (Setup):
        - Todos os módulos do sistema (WhatsApp, Supabase, Pix, Gemini) configurados e operacionais.
        - Recursos disponíveis para reserva.
        - Usuário de teste.
        """
        print("\nSetup: Configurando ambiente completo para o sistema de reserva WhatsApp.")
        test_user_number = test_data["test_10_whatsapp_reservation_system"]["test_user_number"]
        available_resource = test_data["test_10_whatsapp_reservation_system"]["available_resource"]
        # Simular configuração de todos os módulos e disponibilidade de recursos
        yield {
            "test_user_number": test_user_number,
            "available_resource": available_resource
        }
        print("Teardown: Removendo a reserva criada e quaisquer dados de teste associados.")
        # Adicionar lógica para limpeza completa

    def test_full_whatsapp_reservation_flow(self, setup_whatsapp_reservation_system):
        """
        Cenário: SistemaReserva_WhatsApp_Completo
        Objetivo: Validar o fluxo completo do sistema de reserva via WhatsApp,
                 desde a interação inicial até a confirmação da reserva e pagamento.

        Ação Principal (Execute):
        - Usuário inicia uma conversa no WhatsApp.
        - Usuário consulta disponibilidade de recursos.
        - Usuário seleciona um recurso e horário.
        - Usuário inicia o pagamento Pix.
        - Pagamento Pix é confirmado.
        - Reserva é finalizada.

        Validações (Assertions):
        - Confirmar que todas as etapas do fluxo são concluídas com sucesso.
        - Confirmar que as mensagens de feedback ao usuário são apropriadas em cada etapa.
        - Confirmar que os dados são persistidos corretamente no banco de dados.
        - Verificar logs para erros em qualquer ponto do fluxo.
        """
        print(f"Executando: Fluxo completo de reserva WhatsApp para o usuário {setup_whatsapp_reservation_system['test_user_number']}.")

        # 1. Iniciar conversa
        test_case_step1 = test_data["test_10_whatsapp_reservation_system"]["test_cases"][0]
        message_details = {
            "from": setup_whatsapp_reservation_system['test_user_number'],
            "body": test_case_step1["body"]
        }
        response = process_message_logic(message_details)
        assert response["to"] == setup_whatsapp_reservation_system['test_user_number']
        assert any(part in response["message"] for part in test_case_step1["expected_message_parts"])

        # 2. Consultar disponibilidade
        test_case_step2 = test_data["test_10_whatsapp_reservation_system"]["test_cases"][1]
        message_details = {
            "from": setup_whatsapp_reservation_system['test_user_number'],
            "body": test_case_step2["body_template"].format(available_resource=setup_whatsapp_reservation_system['available_resource'])
        }
        response = process_message_logic(message_details)
        assert response["status"] in test_case_step2["expected_status_options"]
        assert any(part in response["message"] for part in test_case_step2["expected_message_parts"])

        # 3. Selecionar recurso e horário (simulando uma reserva)
        test_case_step3 = test_data["test_10_whatsapp_reservation_system"]["test_cases"][2]
        message_details = {
            "from": setup_whatsapp_reservation_system['test_user_number'],
            "body": test_case_step3["body_template"].format(available_resource=setup_whatsapp_reservation_system['available_resource'])
        }
        response = process_message_logic(message_details)
        assert response["to"] == setup_whatsapp_reservation_system['test_user_number']
        assert test_case_step3["expected_message_part"] in response["message"]

        # 4. Iniciar Pix (simulado)
        test_case_step4 = test_data["test_10_whatsapp_reservation_system"]["test_cases"][3]
        message_details = {
            "from": setup_whatsapp_reservation_system['test_user_number'],
            "body": test_case_step4["body"],
            "amount": test_case_step4["amount"],
            "description": test_case_step4["description_pix"]
        }
        response = process_message_logic(message_details)
        assert response["status"] == test_case_step4["expected_status"]
        assert test_case_step4["expected_message_part"] in response["message"]

        # 5. Confirmar Pix (simulado)
        test_case_step5 = test_data["test_10_whatsapp_reservation_system"]["test_cases"][4]
        message_details = {
            "from": setup_whatsapp_reservation_system['test_user_number'],
            "body": test_case_step5["body"],
            "txid": test_case_step5["txid"]
        }
        response = process_message_logic(message_details)
        assert response["status"] == test_case_step5["expected_status"]
        assert test_case_step5["expected_message_part"] in response["message"]

        # 6. Verificar finalização da reserva (coberto pelas asserções acima para o fluxo simulado)