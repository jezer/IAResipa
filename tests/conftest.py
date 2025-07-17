# C:\source\IAResipa\tests\conftest.py

import pytest
import json
from pathlib import Path
from resipaia.A_db.db_00_supabase_config import get_supabase_client

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

@pytest.fixture(scope="function")
def supabase_test_user():
    supabase = get_supabase_client()
    phone_number = "+5511999999999"
    user_data = {"phone_number": phone_number}
    
    # Clean up any existing user with this phone number before the test
    supabase.from_("cadastro_pessoas_fisica").delete().eq("phone_number", phone_number).execute()

    # Insert the test user
    response = supabase.from_("cadastro_pessoas_fisica").insert([user_data]).execute()
    assert response.data is not None and len(response.data) > 0, "Failed to insert test user into Supabase"
    
    yield phone_number

    # Clean up the test user after the test
    supabase.from_("cadastro_pessoas_fisica").delete().eq("phone_number", phone_number).execute()
