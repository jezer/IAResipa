# C:\source\IAResipa\tests\07.organizacaofluxo\test_flow_orchestrator.py

import pytest
from unittest.mock import patch
from resipaia.organizacaofluxo.flow_orchestrator import app

# Define os cenários que este arquivo de teste irá usar
scenarios = [
    "Routing_RegisteredUser",
    "Routing_UnregisteredUser"
]

@pytest.mark.parametrize("scenario_data", scenarios, indirect=True)
class TestFlowOrchestrator:
    """Testes data-driven para o grafo de orquestração de fluxo."""

    def test_routing_scenarios(self, scenario_data):
        """Verifica a lógica de roteamento do grafo com base nos cenários."""
        # Arrange
        initial_state = scenario_data["initial_state"].copy()
        mock_classify_intent_data = scenario_data["mock_classify_intent"]
        mock_check_user_data = scenario_data["mock_check_user"]
        expected_state = scenario_data["expected_state"]

        # Mock das funções dos nós
        with patch('resipaia.organizacaofluxo.flow_orchestrator.classify_intent') as mock_classify,
             patch('resipaia.organizacaofluxo.flow_orchestrator.check_user') as mock_check_user:

            def classify_side_effect(state):
                state.update(mock_classify_intent_data)
                return state
            
            def check_user_side_effect(state):
                state.update(mock_check_user_data)
                return state

            mock_classify.side_effect = classify_side_effect
            mock_check_user.side_effect = check_user_side_effect

            # Act
            final_state = app.invoke(initial_state)

            # Assert
            for key, value in expected_state.items():
                if key == "response_contains":
                    assert value in final_state["response"]
                else:
                    assert final_state[key] == value