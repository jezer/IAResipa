import pytest
import json
import os
from resipaia.interpretartexto.py_main_processor_v2 import process_message_logic

# Carrega os dados de teste do arquivo JSON
current_dir = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(current_dir, "dados", "test_data.json")
with open(data_file_path, 'r', encoding='utf-8') as f:
    test_data = json.load(f)

class TestGeminiIntelligentResponses:
    """
    Testes para validar as respostas inteligentes do Gemini.
    Baseado no cenário: 09.6.gemini_intelligent_responses_scenario.md
    """

    @pytest.fixture(scope="class")
    def setup_gemini_responses(self):
        """
        Pré-condições (Setup):
        - Integração com a API do Gemini configurada e funcional.
        - Base de conhecimento ou dados de treinamento para o Gemini.
        """
        print("\nSetup: Configurando integração com a API do Gemini.")
        # Simular configuração da API do Gemini
        yield
        print("Teardown: Nenhuma ação de limpeza específica necessária.")

    def test_gemini_relevant_response(self, setup_gemini_responses):
        """
        Cenário: Gemini_RespostasInteligentes (Resposta Relevante)
        Objetivo: Validar que o Gemini retorna respostas relevantes e coerentes.

        Ação Principal (Execute):
        - Usuário envia perguntas ou comandos variados ao sistema.
        - Sistema encaminha as interações para o Gemini.

        Validações (Assertions):
        - Confirmar que o Gemini retorna respostas relevantes e coerentes.
        - Verificar logs para erros na comunicação com o Gemini.
        """
        test_case = test_data["test_02_gemini_intelligent_responses"]["test_cases"][0]
        message_details = {
            "from": test_data["test_02_gemini_intelligent_responses"]["user_number"],
            "body": test_case["body"]
        }
        response = process_message_logic(message_details)
        assert response["status"] == test_case["expected_status"]
        assert all(part in response["message"] for part in test_case["expected_message_parts"])

    def test_gemini_ambiguous_response(self, setup_gemini_responses):
        """
        Cenário: Gemini_RespostasInteligentes (Resposta Ambígua)
        Objetivo: Validar que o Gemini lida com perguntas ambíguas ou fora do escopo de forma apropriada.

        Ação Principal (Execute):
        - Usuário envia perguntas ou comandos variados ao sistema.
        - Sistema encaminha as interações para o Gemini.

        Validações (Assertions):
        - Confirmar que o Gemini lida com perguntas ambíguas ou fora do escopo de forma apropriada.
        - Verificar logs para erros na comunicação com o Gemini.
        """
        test_case = test_data["test_02_gemini_intelligent_responses"]["test_cases"][1]
        message_details = {
            "from": test_data["test_02_gemini_intelligent_responses"]["user_number"],
            "body": test_case["body"]
        }
        response = process_message_logic(message_details)
        assert response["status"] == test_case["expected_status"]
        assert any(part in response["message"] for part in test_case["expected_message_parts"])