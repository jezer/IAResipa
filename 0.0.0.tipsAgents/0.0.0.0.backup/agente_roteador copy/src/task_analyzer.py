import google.generativeai as genai
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from models import AgentConfig

@dataclass
class AnalyzedActivity:
    description: str
    required_capabilities: List[str]
    priority: int
    dependencies: List[str] = None
    matched_agent: str = None
    confidence: float = 0.0
    reason_no_match: str = None

class TaskAnalyzer:
    def __init__(self, model: genai.GenerativeModel, available_agents: List[AgentConfig]):
        self.model = model
        self.available_agents = {agent.id: agent for agent in available_agents}
        self.capabilities_map = self._build_capabilities_map()

    def _build_capabilities_map(self) -> Dict[str, List[str]]:
        """
        Cria um mapa de capacidades para cada agente
        """
        capabilities = {}
        for agent_id, agent in self.available_agents.items():
            capabilities[agent_id] = [
                c.lower() for c in agent.capability.split(',')
            ]
        return capabilities

    async def analyze_request(self, content: str) -> Tuple[List[AnalyzedActivity], List[AnalyzedActivity]]:
        """
        Analisa uma solicitação e retorna duas listas:
        1. Atividades que podem ser atendidas
        2. Atividades que não podem ser atendidas
        """
        # Prompt para o Gemini dividir a solicitação em atividades
        activities_prompt = f"""
        Analise a seguinte solicitação e divida-a em atividades distintas e independentes.
        Para cada atividade, identifique:
        1. Descrição clara da atividade
        2. Capacidades necessárias
        3. Prioridade (1-5, onde 1 é mais prioritário)
        4. Dependências (se houver)

        Formato da resposta (JSON):
        {{
            "activities": [
                {{
                    "description": "descrição clara da atividade",
                    "required_capabilities": ["capacidade1", "capacidade2"],
                    "priority": número de 1 a 5,
                    "dependencies": ["id_da_atividade_dependente"] ou null
                }}
            ]
        }}

        Solicitação: {content}
        """

        try:
            response = self.model.generate_content(activities_prompt)
            analyzed = json.loads(response.text)
            
            activities = [
                AnalyzedActivity(
                    description=act["description"],
                    required_capabilities=act["required_capabilities"],
                    priority=act["priority"],
                    dependencies=act.get("dependencies")
                )
                for act in analyzed["activities"]
            ]
            
            return self._match_activities_to_agents(activities)
        except Exception as e:
            logging.error(f"Erro na análise com Gemini: {str(e)}")
            return [], []

    def _match_activities_to_agents(
        self, 
        activities: List[AnalyzedActivity]
    ) -> Tuple[List[AnalyzedActivity], List[AnalyzedActivity]]:
        """
        Tenta corresponder cada atividade com um agente apropriado
        """
        matched = []
        unmatched = []

        for activity in activities:
            best_match = self._find_best_agent_match(activity)
            
            if best_match[0] and best_match[1] >= 0.7:  # Limiar de confiança
                activity.matched_agent = best_match[0]
                activity.confidence = best_match[1]
                matched.append(activity)
            else:
                activity.reason_no_match = self._generate_no_match_reason(
                    activity, best_match[1]
                )
                unmatched.append(activity)

        return matched, unmatched

    def _find_best_agent_match(self, activity: AnalyzedActivity) -> Tuple[str, float]:
        """
        Encontra o melhor agente para uma atividade e retorna (agent_id, confidence)
        """
        best_match = (None, 0.0)

        for agent_id, capabilities in self.capabilities_map.items():
            confidence = self._calculate_match_confidence(
                activity.required_capabilities,
                capabilities
            )
            
            if confidence > best_match[1]:
                best_match = (agent_id, confidence)

        return best_match

    def _calculate_match_confidence(
        self, 
        required: List[str], 
        available: List[str]
    ) -> float:
        """
        Calcula a confiança do match entre capacidades requeridas e disponíveis
        """
        if not required or not available:
            return 0.0

        matches = 0
        total_required = len(required)
        
        for req in required:
            req_lower = req.lower()
            for cap in available:
                # Verifica correspondência exata
                if req_lower == cap.lower():
                    matches += 1
                    break
                # Verifica correspondência parcial
                elif req_lower in cap.lower() or cap.lower() in req_lower:
                    matches += 0.5
                    break

        return matches / total_required

    def _generate_no_match_reason(self, activity: AnalyzedActivity, best_confidence: float) -> str:
        """
        Gera uma explicação detalhada do porquê não houve match
        """
        if best_confidence == 0.0:
            return f"Nenhum agente possui as capacidades necessárias: {', '.join(activity.required_capabilities)}"
        elif best_confidence < 0.7:
            return (f"Melhor correspondência encontrada tem confiança muito baixa ({best_confidence:.2f}). "
                   f"Capacidades necessárias: {', '.join(activity.required_capabilities)}")
        return "Razão desconhecida"
