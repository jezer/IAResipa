import os
import asyncio
import logging
from typing import Dict, Any, Optional
from pathlib import Path
import shutil
import yaml
from datetime import datetime

from .models import (
    AgentType,
    AgentConfig,
    CreatorRequest,
    CreatorResponse,
    TemplateData
)
from .templates import TemplateManager

class AgentCreator:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.template_manager = TemplateManager()
        
        # Garantir que os templates padrão existam
        self.template_manager.create_default_templates()

    async def create_agent(self, request: CreatorRequest) -> CreatorResponse:
        """Cria um novo agente baseado na requisição"""
        try:
            # Validar requisição
            self._validate_request(request)

            # Preparar dados do template
            template_data = TemplateData(
                agent_type=request.agent_type,
                name=request.name,
                description=request.description,
                capabilities=request.capabilities,
                dependencies=self._get_dependencies(request),
                config=request.config,
                metadata=request.metadata
            )

            # Criar diretório do agente
            agent_path = self._create_agent_directory(request.name)

            # Gerar arquivos do agente
            config_files = await self._generate_agent_files(
                agent_path,
                template_data,
                request.template_overrides
            )

            # Configurar ambiente
            await self._setup_environment(agent_path, template_data)

            return CreatorResponse(
                success=True,
                agent_path=str(agent_path),
                config_files=config_files,
                metadata={
                    "created_at": datetime.utcnow().isoformat(),
                    "agent_type": request.agent_type.value,
                    "capabilities": request.capabilities
                }
            )

        except Exception as e:
            self.logger.error(f"Erro ao criar agente: {str(e)}")
            return CreatorResponse(
                success=False,
                error=str(e),
                metadata={"error_type": type(e).__name__}
            )

    def _validate_request(self, request: CreatorRequest) -> None:
        """Valida a requisição de criação de agente"""
        if not request.name or not request.description:
            raise ValueError("Nome e descrição são obrigatórios")

        if not request.capabilities:
            raise ValueError("Pelo menos uma capacidade deve ser especificada")

        # Validar nome do agente
        if not request.name.isidentifier():
            raise ValueError(
                "Nome do agente deve ser um identificador Python válido"
            )

    def _get_dependencies(self, request: CreatorRequest) -> list:
        """Determina as dependências necessárias para o agente"""
        base_deps = ["pydantic", "PyYAML", "aiohttp"]
        
        if request.agent_type == AgentType.MCP_SERVER:
            base_deps.extend(["fastapi", "uvicorn", "python-jose[cryptography]"])
        
        # Adicionar dependências específicas do template
        template_deps = self.config.get("template_dependencies", {}).get(
            request.agent_type.value,
            []
        )
        
        return list(set(base_deps + template_deps))

    def _create_agent_directory(self, agent_name: str) -> Path:
        """Cria a estrutura de diretórios para o novo agente"""
        base_path = Path(self.config.get("agents_path", "agents"))
        agent_path = base_path / agent_name

        # Criar diretórios
        directories = [
            agent_path,
            agent_path / "src",
            agent_path / "tests",
            agent_path / "config",
            agent_path / "docs"
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

        return agent_path

    async def _generate_agent_files(
        self,
        agent_path: Path,
        template_data: TemplateData,
        template_overrides: Optional[Dict[str, str]] = None
    ) -> list:
        """Gera os arquivos do agente usando templates"""
        generated_files = []
        template_files = self.template_manager.get_template_files(
            template_data.agent_type
        )

        # Aplicar overrides de template
        if template_overrides:
            template_files.update(template_overrides)

        # Gerar cada arquivo
        for target_file, template_name in template_files.items():
            try:
                content = self.template_manager.render_template(
                    template_name,
                    template_data
                )
                
                file_path = agent_path / target_file
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(file_path, 'w') as f:
                    f.write(content)
                
                generated_files.append(str(file_path))
                
            except Exception as e:
                self.logger.error(
                    f"Erro ao gerar arquivo {target_file}: {str(e)}"
                )
                raise

        return generated_files

    async def _setup_environment(self, agent_path: Path, template_data: TemplateData) -> None:
        """Configura o ambiente do agente"""
        try:
            # Criar ambiente virtual
            if self.config.get("create_venv", True):
                await self._create_virtual_environment(agent_path)

            # Instalar dependências
            if self.config.get("install_dependencies", True):
                await self._install_dependencies(agent_path)

            # Configurar git se necessário
            if self.config.get("init_git", True):
                await self._init_git_repository(agent_path)

        except Exception as e:
            self.logger.error(f"Erro ao configurar ambiente: {str(e)}")
            raise

    async def _create_virtual_environment(self, agent_path: Path) -> None:
        """Cria um ambiente virtual para o agente"""
        venv_path = agent_path / ".venv"
        
        if not venv_path.exists():
            process = await asyncio.create_subprocess_exec(
                "python", "-m", "venv", str(venv_path),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            await process.communicate()
            
            if process.returncode != 0:
                raise RuntimeError("Falha ao criar ambiente virtual")

    async def _install_dependencies(self, agent_path: Path) -> None:
        """Instala as dependências do agente"""
        requirements_file = agent_path / "requirements.txt"
        venv_pip = agent_path / ".venv" / "Scripts" / "pip"

        if requirements_file.exists():
            process = await asyncio.create_subprocess_exec(
                str(venv_pip), "install", "-r", str(requirements_file),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            await process.communicate()
            
            if process.returncode != 0:
                raise RuntimeError("Falha ao instalar dependências")

    async def _init_git_repository(self, agent_path: Path) -> None:
        """Inicializa um repositório git para o agente"""
        process = await asyncio.create_subprocess_exec(
            "git", "init",
            cwd=str(agent_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        await process.communicate()
        
        if process.returncode != 0:
            raise RuntimeError("Falha ao inicializar repositório git")

        # Criar .gitignore
        gitignore_content = """
.venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
pip-log.txt
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.pytest_cache/
"""
        
        with open(agent_path / ".gitignore", 'w') as f:
            f.write(gitignore_content.strip())
