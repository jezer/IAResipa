import pytest
from src.models import Analysis, RoutingDecision
from src.router import Router

# Dados de configuração mock para os testes
mock_rules_config = {
    "default_rules": {
        "min_confidence": 0.5,
        "fallback_client": "default_client"
    }
}

mock_capabilities_data = {
    "clients": {
        "client_a": {
            "match": {
                "intent": ["code_generation"],
                "domains": ["python"]
            },
            "max_load": 100,
            "current_load": 10
        },
        "default_client": {
            "match": {},
            "max_load": 100,
            "current_load": 20
        }
    }
}

@pytest.fixture
def router_instance():
    """Cria uma instância do Router para os testes."""
    return Router(rules_config=mock_rules_config, capabilities_data=mock_capabilities_data)

def test_router_initialization(router_instance):
    """Testa se o Router é inicializado corretamente."""
    assert router_instance is not None
    assert router_instance.rules == mock_rules_config
    assert router_instance.capabilities == mock_capabilities_data

@pytest.mark.asyncio
async def test_apply_rules_simple_case(router_instance):
    """Testa um caso simples de aplicação de regras."""
    analysis = Analysis(
        intent="code_generation",
        domains=["python"],
        confidence=0.9,
        requires_decomposition=False
    )
    
    # Simula a ausência de um cache para este teste
    router_instance.cache.get = lambda key: None

    decision = await router_instance.apply_rules(analysis, rules=mock_rules_config.get("default_rules", {}))
    
    assert isinstance(decision, RoutingDecision)
    assert decision.result == "valid"
    assert "client_a" in decision.selected_clients
