import os
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from .models import TemplateData, AgentType

class TemplateManager:
    def __init__(self, templates_dir: str = "templates"):
        self.templates_dir = templates_dir
        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def render_template(self, template_name: str, data: TemplateData) -> str:
        """Renderiza um template com os dados fornecidos"""
        template = self.env.get_template(template_name)
        return template.render(data.dict())

    def get_template_files(self, agent_type: AgentType) -> Dict[str, str]:
        """Retorna os templates necessários para um tipo de agente"""
        base_templates = {
            "agent.py": "base/agent.py.j2",
            "config.yaml": "base/config.yaml.j2",
            "requirements.txt": "base/requirements.txt.j2",
            "README.md": "base/readme.md.j2"
        }

        if agent_type == AgentType.MCP_SERVER:
            base_templates.update({
                "router.py": "server/router.py.j2",
                "security.py": "server/security.py.j2",
                "models.py": "server/models.py.j2",
                "api.py": "server/api.py.j2"
            })
        else:  # AgentType.MCP_CLIENT
            base_templates.update({
                "handlers.py": "client/handlers.py.j2",
                "adapters.py": "client/adapters.py.j2"
            })

        return base_templates

    def create_default_templates(self) -> None:
        """Cria os templates padrão se não existirem"""
        templates = {
            # Template base para agent.py
            "base/agent.py.j2": '''from typing import Dict, Any
import asyncio
from .models import *

class {{ name }}:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.capabilities = {{ capabilities }}

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        # Implementar lógica de manipulação de requisições
        pass

    async def start(self):
        # Implementar lógica de inicialização
        pass''',

            # Template para config.yaml
            "base/config.yaml.j2": '''name: {{ name }}
description: {{ description }}
type: {{ agent_type }}
capabilities:
{%- for capability in capabilities %}
  - {{ capability }}
{%- endfor %}
dependencies:
{%- for dep in dependencies %}
  - {{ dep }}
{%- endfor %}
config:
{{ config | yaml }}''',

            # Template para MCPServer específico
            "server/router.py.j2": '''from typing import Dict, Any
from .models import RoutingDecision

class Router:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    async def route_request(self, request: Dict[str, Any]) -> RoutingDecision:
        # Implementar lógica de roteamento
        pass''',

            # Template para MCPClient específico
            "client/handlers.py.j2": '''from typing import Dict, Any

class RequestHandler:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        # Implementar lógica de manipulação
        pass'''
        }

        for path, content in templates.items():
            full_path = Path(self.templates_dir) / path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            if not full_path.exists():
                with open(full_path, 'w') as f:
                    f.write(content)

    def validate_template(self, template_path: str) -> bool:
        """Valida se um template existe e está correto"""
        try:
            self.env.get_template(template_path)
            return True
        except Exception as e:
            print(f"Erro ao validar template {template_path}: {str(e)}")
            return False
