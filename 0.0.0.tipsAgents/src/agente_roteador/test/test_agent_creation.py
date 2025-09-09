
import os
import shutil
import pytest
import yaml
import json
from pathlib import Path
from agente_creator import agente_creator

# Fixture para simular a resposta da API Gemini
@pytest.fixture
def mock_gemini_response(monkeypatch):
    """Mocka a resposta da API do Google Gemini."""
    class MockGenerativeModel:
        def __init__(self, model_name):
            pass

        def generate_content(self, prompt):
            class MockResponse:
                @property
                def text(self):
                    # Retorna uma estrutura JSON baseada no tipo de prompt
                    if "agent.yaml" in prompt:
                        return json.dumps({
                            "scope": {
                                "in_scope": ["Fazer X", "Analisar Y"],
                                "out_of_scope": ["Fazer Z"]
                            },
                            "inputs": [{"type": "text", "description": "Descrição da entrada"}],
                            "outputs": [{"type": "json", "description": "Descrição da saída"}],
                            "constraints": ["Não deve fazer A", "Sempre fazer B"]
                        })
                    elif "prompt.md" in prompt:
                        return json.dumps({
                            "tarefas_principais": ["Tarefa 1", "Tarefa 2"],
                            "fora_do_escopo": ["Não fazer tarefa 3"],
                            "estilo_de_resposta": "Claro e conciso."
                        })
                    return "{}"
            return MockResponse()

    monkeypatch.setattr(agente_creator, 'model', MockGenerativeModel('gemini-pro'))

# Fixture para criar um ambiente de projeto temporário e isolado
@pytest.fixture
def project_root(tmp_path):
    """Cria uma estrutura de diretórios de projeto temporária para os testes."""
    # Define o PROJECT_ROOT para o diretório temporário
    os.environ["PROJECT_ROOT"] = str(tmp_path)
    agente_creator.PROJECT_ROOT = tmp_path

    # Cria a estrutura de diretórios necessária para o agente_creator
    src_dir = tmp_path / "src"
    roteador_dir = src_dir / "agente_roteador"
    roteador_dir.mkdir(parents=True, exist_ok=True)

    # Cria o arquivo base agent.yaml que o creator espera encontrar
    base_agent_yaml_content = {
        "version": "1.0",
        "scope": {},
        "inputs": [],
        "outputs": [],
        "constraints": []
    }
    base_yaml_path = roteador_dir / "agent.yaml"
    with open(base_yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(base_agent_yaml_content, f)
    
    agente_creator.BASE_AGENT_YAML_PATH = base_yaml_path

    # Retorna o caminho raiz do projeto temporário
    yield tmp_path

    # Limpeza: remove a variável de ambiente após o teste
    del os.environ["PROJECT_ROOT"]

def remove_agent(agent_name: str, root_path: Path):
    """Função auxiliar para remover um diretório de agente."""
    agent_dir = root_path / "src" / agent_name
    if agent_dir.exists() and agent_dir.is_dir():
        shutil.rmtree(agent_dir)
        print(f"Agente '{agent_name}' removido de {agent_dir}")
    else:
        print(f"Diretório do agente '{agent_name}' não encontrado em {agent_dir}")


# --- Testes ---

def test_create_agent(project_root, mock_gemini_response):
    """
    Testa a criação de um agente, verificando se o diretório e os arquivos
    são criados como esperado.
    """
    # Arrange: Define os dados do agente a ser criado
    agent_name = "agente_de_teste"
    request_data = {
        "Nome do Agente": agent_name,
        "Objetivo": "Testar a funcionalidade de criação de agentes.",
        "Classificação": "specific",
        "Contexto/Instruções": "Este é um agente de teste."
    }
    
    # Act: Chama a função de criação do agente
    agente_creator.create_agent(request_data)

    # Assert: Verifica se o diretório e os arquivos foram criados
    agent_dir = project_root / "src" / agent_name
    assert agent_dir.exists(), "O diretório do agente deveria ter sido criado."
    assert agent_dir.is_dir(), "O caminho do agente deveria ser um diretório."

    agent_yaml_path = agent_dir / "agent.yaml"
    assert agent_yaml_path.exists(), "O arquivo agent.yaml deveria existir."
    
    prompt_md_path = agent_dir / "prompt.md"
    assert prompt_md_path.exists(), "O arquivo prompt.md deveria existir."

    # Verifica o conteúdo do agent.yaml
    with open(agent_yaml_path, 'r', encoding='utf-8') as f:
        agent_yaml_content = yaml.safe_load(f)
    
    assert agent_yaml_content['name'] == agent_name
    assert "Fazer X" in agent_yaml_content['scope']['in_scope']


def test_remove_agent(project_root, mock_gemini_response):
    """
    Testa a remoção de um agente, primeiro criando-o e depois
    verificando se seu diretório foi removido.
    """
    # Arrange: Cria um agente para poder removê-lo
    agent_name = "agente_para_remover"
    request_data = {
        "Nome do Agente": agent_name,
        "Objetivo": "Um agente que será removido.",
        "Classificação": "specific",
        "Contexto/Instruções": "Criado apenas para teste de remoção."
    }
    agente_creator.create_agent(request_data)
    
    agent_dir = project_root / "src" / agent_name
    assert agent_dir.exists(), "Pré-condição falhou: O diretório do agente não foi criado."

    # Act: Chama a função para remover o agente
    remove_agent(agent_name, project_root)

    # Assert: Verifica se o diretório do agente não existe mais
    assert not agent_dir.exists(), "O diretório do agente deveria ter sido removido."
