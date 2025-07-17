# C:\source\IAResipa\tests\08.responderaoUsuario\test_response_generator.py

import pytest
import json
from unittest.mock import patch, MagicMock

from resipaia.responderaoUsuario.response_generator import (
    classify_intent_with_llm,
    format_response_with_llm
)

# Define os cenários que este arquivo de teste irá usar
scenarios = [
    "ClassifyIntent_Success",
    "ClassifyIntent_JsonError",
    "FormatResponse_Success"
]

@pytest.mark.parametrize("scenario_data", scenarios, indirect=True)
class TestResponseGenerator:
    """Testes data-driven para a lógica de geração de resposta com LLM."""

    @patch('resipaia.responderaoUsuario.response_generator.llm')
    def test_scenarios(self, mock_llm, scenario_data):
        """Executa um cenário de teste com base nos dados carregados."""
        # Arrange: Prepara o estado inicial e o mock do LLM
        initial_state = scenario_data["initial_state"].copy()
        mock_response = scenario_data["mock_llm_response"]
        expected_state = scenario_data["expected_state"]

        if isinstance(mock_response, dict):
            mock_llm.invoke.return_value = MagicMock(content=json.dumps(mock_response))
        else:
            mock_llm.invoke.return_value = MagicMock(content=mock_response)

        # Act: Decide qual função testar com base no nome do cenário
        if "ClassifyIntent" in scenario_data["name"]:
            result_state = classify_intent_with_llm(initial_state)
        elif "FormatResponse" in scenario_data["name"]:
            result_state = format_response_with_llm(initial_state)
        else:
            pytest.fail(f"Cenário de teste não reconhecido: {scenario_data['name']}")

        # Assert: Valida o estado final
        mock_llm.invoke.assert_called_once()
        for key, value in expected_state.items():
            assert result_state[key] == value
