import asyncio
import logging
import yaml
from pathlib import Path
from typing import Dict, Any
from .agent_creator import AgentCreator
from .models import CreatorRequest, CreatorResponse, AgentType

class MCPCreatorClient:
    def __init__(self):
        self.config = self._load_config()
        self.setup_logging()
        self.creator = AgentCreator(self.config)
        self.logger = logging.getLogger(__name__)

    def _load_config(self) -> Dict[str, Any]:
        """Carrega a configuração do agente"""
        config_path = Path(__file__).parent.parent / "config" / "agent.yaml"
        with open(config_path) as f:
            return yaml.safe_load(f)

    def setup_logging(self):
        """Configura o sistema de logging"""
        log_config = self.config.get("logging", {})
        logging.basicConfig(
            level=getattr(logging, log_config.get("level", "INFO")),
            format=log_config.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )

        # Configurar handlers de arquivo se especificado
        for handler_config in log_config.get("handlers", []):
            if handler_config["type"] == "file":
                handler = logging.handlers.RotatingFileHandler(
                    filename=handler_config["filename"],
                    maxBytes=handler_config.get("maxBytes", 1048576),
                    backupCount=handler_config.get("backupCount", 3)
                )
                handler.setLevel(getattr(logging, handler_config.get("level", "INFO")))
                handler.setFormatter(logging.Formatter(log_config.get("format")))
                logging.getLogger().addHandler(handler)

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Manipula requisições MCP"""
        try:
            # Validar requisição
            if "type" not in request or "name" not in request:
                raise ValueError("Requisição deve incluir 'type' e 'name'")

            # Converter para CreatorRequest
            creator_request = CreatorRequest(
                agent_type=AgentType(request["type"]),
                name=request["name"],
                description=request.get("description", f"Agente {request['name']}"),
                capabilities=request.get("capabilities", []),
                config=request.get("config", {}),
                template_overrides=request.get("template_overrides"),
                metadata=request.get("metadata", {})
            )

            # Criar agente
            response = await self.creator.create_agent(creator_request)

            return {
                "success": response.success,
                "agent_path": response.agent_path,
                "config_files": response.config_files,
                "error": response.error,
                "metadata": response.metadata
            }

        except Exception as e:
            self.logger.error(f"Erro ao processar requisição: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "metadata": {"error_type": type(e).__name__}
            }

    async def start(self):
        """Inicializa o cliente MCP"""
        self.logger.info("Iniciando MCPCreatorClient")
        try:
            # Verificar e criar diretórios necessários
            agents_path = Path(self.config.get("agents_path", "agents"))
            agents_path.mkdir(parents=True, exist_ok=True)

            # Verificar templates
            self.creator.template_manager.create_default_templates()

            self.logger.info("MCPCreatorClient iniciado com sucesso")
        except Exception as e:
            self.logger.error(f"Erro ao iniciar MCPCreatorClient: {str(e)}")
            raise

async def main():
    client = MCPCreatorClient()
    await client.start()

    # Exemplo de uso
    request = {
        "type": "mcpclient",
        "name": "exemplo_agente",
        "description": "Um agente de exemplo",
        "capabilities": ["capability1", "capability2"],
        "config": {
            "key": "value"
        }
    }

    response = await client.handle_request(request)
    print(f"Resposta: {response}")

if __name__ == "__main__":
    asyncio.run(main())
