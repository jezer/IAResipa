# C:\source\IAResipa\tests\conftest.py

import pytest
import json
from pathlib import Path

@pytest.fixture(scope="session")
def test_data():
    """Carrega todos os dados de cenários do arquivo JSON."""
    json_path = Path(__file__).parent / "dados" / "test_scenarios_data.json"
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        for name, scenario in data.items():
            scenario['name'] = name
        return data

@pytest.fixture
def scenario_data(request, test_data):
    """Fornece os dados para um cenário de teste específico."""
    scenario_name = request.param
    return test_data[scenario_name]
