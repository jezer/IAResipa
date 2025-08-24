# C:\source\IAResipa\tests\07.organizacaofluxo\test_flow_orchestrator.py

import pytest
import json
from unittest.mock import patch, MagicMock
from resipaia.organizacaofluxo.flow_orchestrator import app, ReservationState, END

# Define os cenários que este arquivo de teste irá usar
scenarios = [
    "Routing_RegisteredUser",
    "Routing_UnregisteredUser"
]

@pytest.mark.parametrize("scenario_data", scenarios, indirect=True)
class TestFlowOrchestrator:
    """Testes data-driven para o grafo de orquestração de fluxo."""

    @patch('resipaia.responderaoUsuario.response_generator.llm')
    def test_routing_scenarios(self, mock_llm, scenario_data, supabase_test_user):
        # Arrange
        initial_state = scenario_data["initial_state"].copy()
        expected_state = scenario_data["expected_state"]

        if scenario_data["name"] == "Routing_RegisteredUser":
            initial_state["phone_number"] = supabase_test_user

        # Configure mocks for LLM calls
        # For classify_intent_with_llm
        mock_llm.invoke.side_effect = [
            MagicMock(content=json.dumps({
                "intent": expected_state["intent"] if "intent" in expected_state else "general_query",
                "sql_query": "SELECT * FROM some_table", # Placeholder, as it's mocked
                "response": None
            })),
            # For format_response_with_llm
            MagicMock(content=expected_state["response"] if "response" in expected_state else "Resposta formatada para:")
        ]

        # Act
        final_state = app.invoke(initial_state)

        # Assert
        for key, value in expected_state.items():
            if key == "user_id":
                assert isinstance(final_state[key], str) # Check if it's a string (UUID)
            elif key == "response_contains":
                assert value in final_state["response"]
            else:
                assert final_state[key] == value