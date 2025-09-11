import logging
import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional
import google.generativeai as genai
from datetime import datetime
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from .models import MCPRequest, MCPResponse, Analysis
from .router import Router
from .security import SecurityLayer
from .adapters import GeminiAdapter, ClaudeAdapter, CopilotAdapter, CursorAdapter
from cryptography.fernet import Fernet
from jwt import encode, decode
import logging.config
import os
import re

# Adicionando imports para os novos módulos de comando
from agente_creator import agente_creator
from agente_remover import remover


logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'secure_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'secure.log',
            'maxBytes': 1024*1024,
            'backupCount': 3,
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {
            'handlers': ['secure_file'],
            'level': 'INFO',
        },
    },
}

api_key_header = APIKeyHeader(name="X-API-Key")

# Initialize FastAPI app
app = FastAPI(
    title="MCP Server",
    description="Message Control & Processing Server",
    version="1.0.0"
)

class MCPServer:
    def __init__(self, config_dir: Optional[Path] = None):
        self.app = app
        self.config_dir = config_dir or Path(__file__).parent / "config"
        self.config = self._load_configurations()
        
        # Configura a chave de API do Gemini
        genai.configure(api_key=self.config["gemini_api_key"])

        # Inicialização do Gemini-Flash para análise rápida
        self.gemini_flash = genai.GenerativeModel(
            model_name="gemini-pro",
            generation_config={
                'temperature': 0.1,  # Baixa temperatura para respostas determinísticas
                'top_p': 0.1,       # Foco nas previsões mais prováveis
                'max_output_tokens': 150  # Limitar tamanho para velocidade
            }
        )
        
        self.router = self._initialize_router()
        
        # Configurar logging
        logging.basicConfig(
            level=self.config.get("log_level", logging.INFO),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Inicializar adaptadores
        self.llm_adapters = {
            "gemini": GeminiAdapter(),
            "claude": ClaudeAdapter(),
            "copilot": CopilotAdapter(),
            "cursor": CursorAdapter()
        }

        # Inicializar camada de segurança
        self.security_layer = SecurityLayer(secret_key="test-secret")

        self.setup_routes()

    def setup_routes(self):
        @self.app.post("/analyze")
        async def analyze_route(
            request: MCPRequest,
            api_key: str = Security(api_key_header)
        ):
            if not self.security_layer.validate_api_key(api_key):
                raise HTTPException(status_code=403)
            
            return await self.handle_request(request)

    def _load_configurations(self):
        """Carrega todas as configurações externas"""
        config_path = self.config_dir / "sources.yaml"
        
        with open(config_path, "r") as f:
            config_sources = yaml.safe_load(f)
        
        return {
            "capabilities": self._load_yaml(self.config_dir / config_sources["capabilities"]),
            "routing_rules": self._load_markdown(self.config_dir / config_sources["routing_rules"]),
            "prompts": self._load_markdown(self.config_dir / config_sources["gemini_prompts"]),
            "gemini_api_key": config_sources["gemini_api_key"]
        }

    def _initialize_router(self) -> Router:
        return Router(self.config["routing_rules"], self.config["capabilities"])

    def _initialize_project_root_for_modules(self):
        """Garante que o PROJECT_ROOT esteja definido para os módulos de comando."""
        # This path navigates from src/agente_roteador/src up to the root directory
        project_root_path = Path(__file__).parent.parent.parent 
        
        if not os.getenv("PROJECT_ROOT"):
            os.environ["PROJECT_ROOT"] = str(project_root_path)
        
        # Atualiza os módulos que dependem do PROJECT_ROOT
        agente_creator.PROJECT_ROOT = project_root_path
        # Garante que o caminho base do YAML para o criador seja absoluto
        agente_creator.BASE_AGENT_YAML_PATH = project_root_path / "src" / "agente_roteador" / "agent.yaml"
        remover.PROJECT_ROOT = project_root_path


    async def handle_request(self, request: MCPRequest) -> MCPResponse:
        try:
            content = request.content.strip()

            # --- INÍCIO DA NOVA LÓGICA DE COMANDO ---
            if content.startswith("comando:"):
                self._initialize_project_root_for_modules()

                # Comando de Criação
                if "criar agente" in content:
                    try:
                        # Extrai o JSON da string. Ex: "comando: criar agente { ... }"
                        json_str_match = re.search(r'\{.*\}', content, re.DOTALL)
                        if not json_str_match:
                            raise ValueError("Nenhum objeto JSON encontrado no comando de criação.")
                        
                        request_data = json.loads(json_str_match.group(0))
                        
                        if "Nome do Agente" not in request_data or "Objetivo" not in request_data:
                            raise ValueError("Dados insuficientes. 'Nome do Agente' e 'Objetivo' são obrigatórios.")

                        agente_creator.create_agent(request_data)
                        return MCPResponse(success=True, content=f"Comando de criação para '{request_data.get('Nome do Agente')}' processado com sucesso.")

                    except Exception as e:
                        logging.error(f"Erro no comando de criação de agente: {e}")
                        return await self._handle_error(e)

                # Comando de Remoção
                elif "remover agente" in content:
                    try:
                        # Extrai o nome do agente. Ex: "comando: remover agente nome_do_agente"
                        agent_name = content.split("remover agente", 1)[1].strip()
                        if not agent_name:
                            raise ValueError("Nome do agente não especificado para remoção.")
                        
                        result = remover.remove_agent(agent_name)
                        
                        success = result.get("status") == "sucesso"
                        return MCPResponse(success=success, content=result.get("message"), metadata=result)

                    except Exception as e:
                        logging.error(f"Erro no comando de remoção de agente: {e}")
                        return await self._handle_error(e)
                
                else:
                    return MCPResponse(success=False, content="Comando desconhecido.", error="Comando não suportado após 'comando:'.")
            # --- FIM DA NOVA LÓGICA DE COMANDO ---

            # Se não for um comando, segue o fluxo original de análise por IA
            llm_source = request.headers.get("X-LLM-Source", "default")
            llm_capabilities = request.headers.get("X-LLM-Capabilities", [])
            
            analysis = await self._analyze_with_llm(
                llm_source=llm_source,
                capabilities=llm_capabilities,
                template=self.config["prompts"]["análise_solicitação"],
                context={
                    "available_capabilities": self.config["capabilities"],
                    "llm_context": request.context
                },
                content=request.content
            )

            routing_decision = self.router.apply_rules(
                analysis=analysis,
                rules=self.config["routing_rules"],
                llm_context={
                    "source": llm_source,
                    "capabilities": llm_capabilities
                }
            )

            if routing_decision.is_valid():
                response = await self._process_valid_routing(routing_decision)
            else:
                response = await self._handle_fallback(request, analysis)

            formatted_response = await self._format_response(response, llm_source)
            
            return MCPResponse(
                success=True,
                content=formatted_response,
                metadata={
                    "routing_decision": routing_decision.dict(),
                    "llm_source": llm_source
                }
            )

        except Exception as e:
            logging.error(f"Erro ao processar requisição: {str(e)}")
            return await self._handle_error(e)

    async def _analyze_with_llm(self, llm_source: str, capabilities: list,
                              template: str, context: dict, content: str) -> Analysis:
        """Análise adaptada ao LLM fonte"""
        try:
            if llm_source == "gemini":
                return await self._analyze_with_gemini_flash(content, context)
            else:
                # Fallback para análise padrão para outros LLMs
                return await self._analyze_standard(content, context)
        except Exception as e:
            logging.error(f"Erro na análise com LLM {llm_source}: {str(e)}")
            raise

    async def _analyze_with_gemini_flash(self, content: str, context: dict) -> Analysis:
        """Análise rápida usando Gemini-Flash"""
        prompt = self._build_flash_prompt(content, context)
        response = await self.gemini_flash.generate_content_async(
            prompt,
            generation_config={
                'candidate_count': 1,
                'stop_sequences': ["}"]
            }
        )
        return self._parse_flash_response(response)

    async def _format_response(self, response: MCPResponse, llm_source: str) -> Dict:
        """Formata a resposta de acordo com o LLM fonte"""
        adapter = self.llm_adapters.get(llm_source)
        if not adapter:
            raise ValueError(f"LLM não suportado: {llm_source}")
        return await adapter.format_response(response)

    def _build_flash_prompt(self, content: str, context: dict) -> str:
        # Implementar construção do prompt
        return f"""
        SYSTEM
        Você é um analisador rápido e preciso.
        Analise a solicitação e retorne apenas JSON.

        CONTEXT
        {json.dumps(context)}

        USER_REQUEST
        {content}
        """

    def _parse_flash_response(self, response) -> Analysis:
        # Implementar parsing da resposta
        try:
            content = response.text
            data = json.loads(content)
            return Analysis(**data)
        except Exception as e:
            logging.error(f"Erro ao fazer parse da resposta: {str(e)}")
            raise

    @staticmethod
    def _load_yaml(path: Path) -> Dict:
        """Load YAML file from absolute path"""
        with open(path) as f:
            return yaml.safe_load(f)

    @staticmethod
    def _load_markdown(path: Path) -> str:
        """Load Markdown file from absolute path"""
        with open(path) as f:
            return f.read()

    async def _handle_error(self, error: Exception) -> MCPResponse:
        return MCPResponse(
            success=False,
            content=str(error),
            metadata={"error_type": error.__class__.__name__}
        )



class AuditTrail:
    def log_access(self, request: MCPRequest):
        log_entry = {
            "timestamp": datetime.utcnow(),
            "source_llm": request.source,
            "request_id": hash(request),
            "action": "analyze"
        }
        logging.info("Access logged", extra=log_entry)


if __name__ == "__main__":
    import uvicorn
    server = MCPServer()
    uvicorn.run(server.app, host="0.0.0.0", port=8000)