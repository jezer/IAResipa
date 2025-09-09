import pytest
import json
import os
from pathlib import Path
from fastapi.testclient import TestClient
import yaml

# Adiciona o diretório raiz ao sys.path para encontrar os módulos
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agente_roteador.src.server import app
from agente_creator import agente_creator

@pytest.fixture(scope="module")
def test_client():
    """Cria um cliente de teste para a aplicação FastAPI."""
    with TestClient(app) as client:
        yield client

@pytest.fixture(autouse=True)
def project_structure(tmp_path, monkeypatch):
    """
    Cria uma estrutura de projeto real para teste de integração
    """
    # 1. Define o PROJECT_ROOT para o diretório temporário
    project_root = tmp_path
    monkeypatch.setenv("PROJECT_ROOT", str(project_root))

    # 2. Cria a estrutura de diretórios e arquivos de configuração
    config_dir = project_root / "src" / "agente_roteador" / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    
    # 3. Cria arquivos de configuração necessários
    config_files = {
        "sources.yaml": {
            "capabilities": "capabilities.yaml",
            "routing_rules": "routing_rules.yaml",
            "gemini_prompts": "prompts.md",
            "gemini_api_key": "YOUR_REAL_GEMINI_API_KEY",  # Substitua pela sua chave real
            "openai_api_key": "YOUR_REAL_OPENAI_KEY"       # Substitua pela sua chave real
        },
        "capabilities.yaml": {
            "clients": {
                "default_client": {
                    "type": "openai",
                    "capabilities": ["text_generation", "code_generation"],
                    "confidence_threshold": 0.5
                }
            }
        },
        "routing_rules.yaml": {
            "default_rules": {
                "min_confidence": 0.5,
                "fallback_client": "default_client"
            }
        }
    }
    
    # Escreve os arquivos de configuração
    for filename, content in config_files.items():
        with open(config_dir / filename, 'w', encoding='utf-8') as f:
            yaml.dump(content, f)
    
    # Cria o arquivo de prompts
    prompts_content = """
    # Agente Creator Prompts
    ## Default
    Você é um assistente especializado em criar e gerenciar agentes.
    """
    (config_dir / "prompts.md").write_text(prompts_content)

    # 4. Cria o arquivo base agent.yaml no diretório do agente roteador
    base_agent_yaml_content = {"version": "1.0"}
    base_yaml_path = project_root / "src" / "agente_roteador" / "agent.yaml"
    with open(base_yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(base_agent_yaml_content, f)
    
    return project_root

# --- Teste de Integração ---

def test_create_and_remove_agent_via_server(test_client, project_structure):
    """
    Testa o fluxo completo de ponta a ponta sem mocks
    """
    agent_name = "agente_qualidade"
    project_root = project_structure
    agent_dir = project_root / "src" / agent_name

    # --- Parte 1: Teste de Criação do Agente ---
    
    # Arrange (Preparação)
    creation_payload = {
        "Nome do Agente": agent_name,
        "Objetivo": "Avaliar a qualidade de outros agentes com base em métricas.",
        "Classificação": "utility",
        "Contexto/Instruções": "Este agente executa testes e gera relatórios de qualidade."
    }
    creation_command = f"comando: criar agente {json.dumps(creation_payload)}"

    # Act (Ação)
    response_create = test_client.post(
        "/analyze",
        json={"content": creation_command, "source": "test_client"},
        headers={"X-API-Key": "test_key"} # A chave é validada no servidor
    )

    # Assert (Verificação da Criação)
    assert response_create.status_code == 200
    response_json = response_create.json()
    assert response_json["success"] is True
    assert f"processado com sucesso" in response_json["content"]
    
    # Verifica se o diretório e os arquivos foram REALMENTE criados
    assert agent_dir.exists(), f"O diretório do agente '{agent_name}' deveria ter sido criado em {agent_dir}"
    assert (agent_dir / "agent.yaml").exists(), "O arquivo agent.yaml não foi encontrado."
    assert (agent_dir / "prompt.md").exists(), "O arquivo prompt.md não foi encontrado."

    print(f"\nSUCESSO: Agente '{agent_name}' criado com sucesso via servidor.")

    # --- Parte 2: Teste de Remoção do Agente ---

    # Arrange
    removal_command = f"comando: remover agente {agent_name}"

    # Act
    response_remove = test_client.post(
        "/analyze",
        json={"content": removal_command, "source": "test_client"},
        headers={"X-API-Key": "test_key"}
    )

    # Assert (Verificação da Remoção)
    assert response_remove.status_code == 200
    response_json = response_remove.json()
    assert response_json["success"] is True
    assert "removido com sucesso" in response_json["content"]

    # Verifica se o diretório foi REALMENTE removido
    assert not agent_dir.exists(), f"O diretório do agente '{agent_name}' deveria ter sido removido de {agent_dir}"

    print(f"SUCESSO: Agente '{agent_name}' removido com sucesso via servidor.")
