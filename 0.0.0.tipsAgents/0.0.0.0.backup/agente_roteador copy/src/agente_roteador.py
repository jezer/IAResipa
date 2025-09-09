import json
import datetime
import logging
import os
import uuid
import google.generativeai as genai
from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Union
from enum import Enum
from pathlib import Path
from dotenv import load_dotenv

# Configuração do Gemini
from dotenv import load_dotenv
from pathlib import Path

# Carrega o .env a partir da raiz do projeto
load_dotenv() 
PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT"))

GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("A variável de ambiente GEMINI_API_KEY não foi encontrada.")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

class AgentType(Enum):
    GLOBAL = "global"
    SPECIFIC = "specific"

class CommunicationType(Enum):
    SYNC = "synchronous_python_call"
    ASYNC = "asynchronous_file_transfer"

@dataclass
class Agent:
    id: str
    type: AgentType
    capabilities: List[str]
    in_scope: List[str]
    out_of_scope: List[str]
    communication_channels: List[str]
    inputs: List[Dict[str, str]]
    outputs: List[Dict[str, str]]
    constraints: List[str]

import yaml
import markdown
from typing import Dict, Any

class RouterConfig:
    def __init__(self):
        self.config = self.load_agent_config()
        self.prompt_template = self.load_prompt_template()
        self.setup_logging()
        
    def load_agent_config(self) -> Dict[str, Any]:
        """Carrega a configuração do agente do arquivo YAML local."""
        config_path = Path(__file__).parent / "agent.yaml"
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            
        self.GLOBAL_AGENTS = {}
        self.SPECIFIC_AGENTS = {}
        
        for agent_id in config.get('dependencies', []):
            agent_info = self.get_agent_capabilities(agent_id)
            
            if agent_info:
                if agent_info.type == AgentType.GLOBAL:
                    self.GLOBAL_AGENTS[agent_id] = agent_info
                else:
                    self.SPECIFIC_AGENTS[agent_id] = agent_info
                
        return config
    
    def get_agent_capabilities(self, agent_id: str) -> Optional[Agent]:
        """Carrega as capacidades de um agente a partir de seu arquivo de configuração em src/."""
        try:
            agent_folder_name = agent_id
            agent_config_path = PROJECT_ROOT / "src" / agent_folder_name / "agent.yaml"

            if agent_config_path.exists():
                with open(agent_config_path, 'r', encoding='utf-8') as f:
                    agent_config = yaml.safe_load(f)
                    agent_type_str = agent_config.get('type', 'specific')
                    agent_type = AgentType(agent_type_str)

                    return Agent(
                        id=agent_id,
                        type=agent_type,
                        capabilities=agent_config.get('scope', {}).get('in_scope', []),
                        in_scope=agent_config.get('scope', {}).get('in_scope', []),
                        out_of_scope=agent_config.get('scope', {}).get('out_of_scope', []),
                        communication_channels=agent_config.get('communication_channels', []),
                        inputs=agent_config.get('inputs', []),
                        outputs=agent_config.get('outputs', []),
                        constraints=agent_config.get('constraints', [])
                    )
        except Exception as e:
            logging.warning(f"Não foi possível carregar configuração para {agent_id}: {e}")
        
        return None
    
    def setup_logging(self):
        log_dir = PROJECT_ROOT / "logs" / "routing"
        os.makedirs(log_dir, exist_ok=True)
        logging.basicConfig(
            filename=f"{log_dir}/router_{datetime.datetime.now().strftime('%Y%m%d')}.ndjson",
            level=logging.INFO,
            format='{"timestamp": "% (asctime)s", "level": "% (levelname)s", "message": % (message)s}'
        )

async def route_request(user_prompt: str, return_type: str = "json") -> dict:
    """
    Analisa um prompt do usuário e determina a decisão de roteamento apropriada usando o Gemini.
    """
    router = RouterConfig()
    available_agents = {**router.GLOBAL_AGENTS, **router.SPECIFIC_AGENTS}
    
    rejection_policies = router.config.get('policies', {}).get('rejection', [])
    
    try:
        gemini_response = await router.analyze_prompt_with_gemini(user_prompt, available_agents)
        
        if gemini_response.get("decision_type") == "create":
            create_request = {
                "action": "route",
                "tasks": [{
                    "target_agent": "agente_creator",
                    "content": gemini_response.get("create_agent_request"),
                    "reason": "Necessidade de criar novo agente identificada"
                }]
            }
            logging.info(f"Solicitando criação de novo agente: {json.dumps(create_request, indent=2)}")
            return create_request
            
        elif gemini_response.get("decision_type") == "reject":
            suggestion = next(
                (policy for policy in rejection_policies if "sugerir criação" in policy.lower()),
                "Sugerir consulta ao agente_creator para análise de viabilidade"
            )
            return {
                "action": "reject",
                "reason": gemini_response.get("rejection_reason"),
                "suggestion": suggestion
            }
            
        return {
            "action": gemini_response.get("decision_type"),
            "tasks": gemini_response.get("tasks")
        }
            
    except Exception as e:
        logging.error(f"Erro ao processar solicitação: {str(e)}")
        return {
            "action": "reject",
            "reason": f"Erro interno: {str(e)}",
            "suggestion": "Por favor, tente novamente ou contate o administrador"
        }

    def load_prompt_template(self) -> str:
        """Carrega o template do prompt do arquivo MD local."""
        prompt_path = Path(__file__).parent / "prompt.md"
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()

    async def analyze_prompt_with_gemini(self, prompt: str, available_agents: Dict[str, Agent]) -> Dict:
        """Analisa o prompt usando o Gemini para identificar tarefas e agentes necessários"""
        
        agent_descriptions = []
        for agent_id, agent in available_agents.items():
            description = (
                f"- {agent_id}:\n"
                f"  Capacidades: {', '.join(agent.capabilities)}\n"
                f"  Escopo: {', '.join(agent.in_scope)}\n"
                f"  Fora do Escopo: {', '.join(agent.out_of_scope)}\n"
                f"  Canais de Comunicação: {', '.join(agent.communication_channels)}\n"
                f"  Restrições: {', '.join(agent.constraints)}\n"
            )
            agent_descriptions.append(description)
        
        gemini_prompt = f'''
        {self.prompt_template}

        INSTRUÇÕES IMPORTANTES:
        1. Se a solicitação não se encaixar em nenhum agente existente, você DEVE sugerir a criação de um novo agente
        2. Ao sugerir um novo agente, siga ESTRITAMENTE o formato do guia de criação de agentes
        3. Para tarefas complexas, você pode dividir entre múltiplos agentes existentes

        Se for necessário criar um novo agente, use este formato:
        {{
            "decision_type": "create",
            "create_agent_request": {{
                "Classificação": "Global|Específico",
                "Nome do Agente": "nome_do_agente",
                "Objetivo": "Objetivo claro e conciso",
                "Contexto/Instruções": "Instruções detalhadas seguindo o template"
            }},
            "reason": "Explicação detalhada da necessidade"
        }}

        Agentes disponíveis e suas capacidades:
        {chr(10).join(agent_descriptions)}

        Solicitação do usuário: "{prompt}"

        Responda em formato JSON com a seguinte estrutura:
        {{
            "decision_type": "single|split|reject|create",
            "tasks": [
                {{
                    "target_agent": "id_do_agente",
                    "action": "ação_específica",
                    "reason": "motivo_detalhado"
                }}
            ],
            "rejection_reason": "se aplicável",
            "create_agent_request": {{}} // obrigatório se decision_type for "create"
        }}
        '''
        
        try:
            response = model.generate_content(gemini_prompt)
            result = json.loads(response.text)
            
            if not isinstance(result, dict) or "decision_type" not in result:
                raise ValueError("Resposta do Gemini em formato inválido")
                
            if result["decision_type"] == "create" and "create_agent_request" in result:
                result["original_prompt"] = prompt
                
            return result
            
        except Exception as e:
            logging.error(f"Erro ao processar com Gemini: {str(e)}")
            return self.analyze_prompt_with_keywords(prompt)
            
    def analyze_prompt_with_keywords(self, prompt: str) -> Dict:
        """Método de fallback que usa keywords para análise do prompt"""
        keywords = {
            "criar agente": {"agent": "agente_creator", "action": "agent_creation"},
            "qualidade": {"agent": "agente_quality", "action": "quality_check"},
            "auditar": {"agent": "agente_quality", "action": "audit"},
            "fluxo": {"agent": "agente_fluxos", "action": "flow_creation"},
            "diagrama": {"agent": "agente_fluxos", "action": "diagram_creation"},
            "plano de testes": {"agent": "agente_testes", "action": "test_planning"},
            "cenarios de testes": {"agent": "agente_testes", "action": "test_scenarios"}
        }
        
        tasks = []
        prompt_lower = prompt.lower()
        
        for key, info in keywords.items():
            if key in prompt_lower:
                tasks.append({
                    "target_agent": info["agent"],
                    "action": info["action"],
                    "content": prompt,
                    "reason": f"Correspondência por palavra-chave: '{key}'"
                })
        
        if not tasks:
            return {
                "decision_type": "reject",
                "rejection_reason": "Nenhum agente compatível encontrado via palavras-chave",
                "tasks": []
            }
            
        return {
            "decision_type": "single" if len(tasks) == 1 else "split",
            "tasks": tasks
        }

    logging.info(json.dumps({"event": "routing_request", "prompt": user_prompt}))
    
    tasks = await analyze_prompt_with_gemini(user_prompt, available_agents)

    routing_decision = {
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "user_id": "anon",
        "prompt": user_prompt,
        "router_decision": {
            "type": "reject",
            "targets": []
        },
        "reason": "Nenhum agente compatível encontrado."
    }

    if not tasks:
        logging.info(json.dumps({
            "event": "routing_rejected",
            "reason": "No matching agents",
            "prompt": user_prompt
        }))
        
        routing_decision["suggestion"] = (
            "Posso solicitar ao agente_creator que analise "
            "a viabilidade de criar um novo agente para esta função?"
        )
        
    elif len(tasks) == 1:
        task = tasks[0]
        if task["target_agent"] in available_agents:
            routing_decision["router_decision"]["type"] = "single"
            routing_decision["router_decision"]["targets"] = [task["target_agent"]]
            routing_decision["reason"] = task["reason"]
            
            logging.info(json.dumps({
                "event": "routing_single",
                "target": task["target_agent"],
                "reason": task["reason"]
            }))
            
    else:
        routing_decision["router_decision"]["type"] = "split"
        routing_decision["router_decision"]["targets"] = [
            task["target_agent"] for task in tasks
        ]
        routing_decision["reason"] = "Multiple agents required for complex task"
        routing_decision["tasks"] = tasks
        
        logging.info(json.dumps({
            "event": "routing_split",
            "targets": routing_decision["router_decision"]["targets"],
            "task_count": len(tasks)
        }))

    if return_type == "file":
        output_path = "output/routing_decision.json"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(routing_decision, f, ensure_ascii=False, indent=2)
        return {"status": "success", "file": output_path}

    return routing_decision

def validate_routing_schema(routing_decision: dict) -> bool:
    """Validates that the routing decision matches the required schema"""
    required_fields = ["ts", "user_id", "prompt", "router_decision", "reason"]
    decision_fields = ["type", "targets"]
    
    if not all(field in routing_decision for field in required_fields):
        return False
        
    decision = routing_decision["router_decision"]
    if not all(field in decision for field in decision_fields):
        return False
        
    if decision["type"] not in ["single", "split", "reject"]:
        return False
        
    if decision["type"] in ["single", "split"] and not decision["targets"]:
        return False
        
    return True

if __name__ == "__main__":
    import asyncio
    
    async def run_tests():
        print("Testando agente_roteador com Gemini:")

        test_cases = [
            {
                "prompt": "Preciso criar um novo agente para gerenciar pedidos.",
                "return_type": "json"
            },
            {
                "prompt": "Verifique a qualidade do código e auditar as regras.",
                "return_type": "file"
            },
            {
                "prompt": "Preciso um fluxo de processo e plano de testes para o módulo de login.",
                "return_type": "json"
            },
            {
                "prompt": "Qual é a previsão do tempo para amanhã?",
                "return_type": "json"
            }
        ]

        for case in test_cases:
            print(f"\nTestando prompt: '{case['prompt']}'")
            result = await route_request(case["prompt"], case["return_type"])
            
            if case["return_type"] == "json":
                if validate_routing_schema(result):
                    print("Schema: Válido")
                else:
                    print("Schema: Inválido")
                    
                print(f"Decisão de Roteamento: {json.dumps(result, indent=2, ensure_ascii=False)}")
            else:
                print(f"Arquivo gerado: {result.get('file')}")

    asyncio.run(run_tests())