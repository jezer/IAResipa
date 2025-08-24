import pytest
import json
from resipaia.interpretartexto.py_main_processor_v2 import process_message_logic

# Carrega os dados de teste do arquivo JSON
with open("C:\source\IAResipa\tests\06\interpretartexto\dados\test_data.json", 'r', encoding='utf-8') as f:
    test_data = json.load(f)

class TestGeminiGeneralQuery:
    """
    Testes para validar a resposta do Gemini a consultas gerais.
    """

    @pytest.fixture(scope="class")
    def setup_user(self):
        """
        Pré-condições (Setup):
        - Usuário de teste.
        """
        print("\nSetup: Configurando usuário de teste para consulta Gemini.")
        user_id = test_data["test_gemini_general_query"]["user_id"]
        yield {"user_id": user_id}
        print("Teardown: Limpeza de usuário de teste.")

    def test_general_query_response(self, setup_user):
        """
        Cenário: Consulta Geral ao Gemini
        Objetivo: Validar que o Gemini responde a uma pergunta geral de forma coerente e não vazia.

        Ação Principal (Execute):
        - Usuário envia uma pergunta geral ao sistema.

        Validações (Assertions):
        - Confirmar que o status da resposta é 'success'.
        - Confirmar que a mensagem de resposta não está vazia.
        """
        test_case = test_data["test_gemini_general_query"]["test_cases"][0]
        message_details = {
            "from": setup_user['user_id'],
            "body": test_case["body"]
        }
        response = process_message_logic(message_details)
        assert response["status"] == test_case["expected_status"]
        if test_case["expected_message_not_empty"]:
            assert response["message"] is not None and response["message"] != ""