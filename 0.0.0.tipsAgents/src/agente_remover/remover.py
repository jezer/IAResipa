import shutil
from pathlib import Path
import os

# Garante que o PROJECT_ROOT seja carregado a partir de variáveis de ambiente ou um padrão
PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT", Path(__file__).parent.parent))

def remove_agent(agent_name: str):
    """
    Localiza e remove o diretório de um agente com base no nome.

    Args:
        agent_name (str): O nome do agente a ser removido.

    Returns:
        dict: Um dicionário com o status e uma mensagem.
    """
    if not agent_name or not isinstance(agent_name, str):
        return {"status": "erro", "message": "Nome do agente inválido."}

    # O diretório dos agentes é sempre dentro de 'src'
    agent_dir = PROJECT_ROOT / "src" / agent_name.strip()

    if agent_dir.exists() and agent_dir.is_dir():
        try:
            shutil.rmtree(agent_dir)
            return {"status": "sucesso", "message": f"Agente '{agent_name}' e seu diretório foram removidos com sucesso de {agent_dir}."}
        except OSError as e:
            return {"status": "erro", "message": f"Erro ao remover o diretório {agent_dir}: {e}"}
    else:
        return {"status": "erro", "message": f"Agente '{agent_name}' não encontrado no diretório {agent_dir}."}
