import logging
from typing import Dict, Any, List
from datetime import datetime
import uuid
import hashlib
import json
from .models import RoutingDecision, Analysis, SubTask, TaskStatus
from .cache import Cache

class Router:
    def __init__(self, rules_config: Dict[str, Any], capabilities_data: Dict[str, Any]):
        self.rules = rules_config
        self.capabilities = capabilities_data
        self.logger = logging.getLogger(__name__)
        self.cache = Cache()
        self._subtasks: Dict[str, SubTask] = {}

    async def apply_rules(self, analysis: Analysis, rules: Dict[str, Any], llm_context: Dict[str, Any] = None) -> RoutingDecision:
        """Aplica regras de roteamento com suporte a decomposição de tarefas"""
        
        # Verificar cache primeiro
        cache_key = self._generate_cache_key(analysis, llm_context)
        cached_decision = self.cache.get(cache_key)
        if cached_decision:
            return cached_decision

        # Calcular pontuação base
        score = await self._calculate_base_score(analysis, rules)

        # Aplicar regras específicas do LLM
        if llm_context:
            score = await self._apply_llm_specific_rules(score, llm_context)

        # Verificar necessidade de decomposição
        subtasks = []
        if analysis.requires_decomposition:
            subtasks = await self._create_subtasks(analysis)

        # Selecionar clientes apropriados
        selected_clients = await self._select_clients(analysis, score, subtasks)

        # Criar decisão de roteamento
        decision = RoutingDecision(
            request_id=str(uuid.uuid4()),
            rules_used=self._get_applied_rules(analysis, rules),
            confidence=min(1.0, score),
            result="valid" if score >= 0.4 else "fallback",
            selected_clients=selected_clients,
            metadata={
                "subtasks": [task.dict() for task in subtasks],
                "timestamp": datetime.utcnow().isoformat(),
                "analysis_summary": analysis.dict()
            }
        )

        # Armazenar no cache
        self.cache.set(cache_key, decision)

        self._log_decision(decision)
        return decision

    async def _apply_llm_specific_rules(self, score: float, llm_context: Dict[str, Any]) -> float:
        """Aplica regras específicas do LLM"""
        source = llm_context.get("source")
        capabilities = llm_context.get("capabilities", [])

        # Bônus por fonte confiável
        if source in ["gemini", "copilot", "cursor"]:
            score += 0.1

        # Bônus por capabilities relevantes
        if "code_analysis" in capabilities:
            score += 0.1
        if "task_decomposition" in capabilities:
            score += 0.1

        return score

    async def _select_clients(self, analysis: Analysis, score: float, subtasks: List[SubTask]) -> List[str]:
        """Seleciona clientes apropriados baseado na análise e subtarefas"""
        selected_clients = set()

        # Selecionar clientes para a tarefa principal
        main_clients = self._select_clients_for_task(analysis)
        selected_clients.update(main_clients)

        # Selecionar clientes para subtarefas
        for subtask in subtasks:
            if subtask.target_client_id:
                selected_clients.add(subtask.target_client_id)
            else:
                task_clients = self._select_clients_for_task(Analysis(
                    intent=subtask.intent,
                    domains=subtask.domains,
                    confidence=score
                ))
                selected_clients.update(task_clients)

        return list(selected_clients)

    def _select_clients_for_task(self, analysis: Analysis) -> List[str]:
        """Seleciona clientes para uma tarefa específica"""
        selected_clients = []

        for client_id, client_info in self.capabilities.get("clients", {}).items():
            match_criteria = client_info.get("match", {})
            
            # Verificar correspondência de intent
            intent_match = (
                analysis.intent in match_criteria.get("intent", [])
                if match_criteria.get("intent")
                else False
            )

            # Verificar correspondência de domínios
            domain_match = any(
                domain in match_criteria.get("domains", [])
                for domain in analysis.domains
            ) if match_criteria.get("domains") else False

            # Verificar carga atual do cliente
            if client_info.get("current_load", 0) >= client_info.get("max_load", 100):
                continue

            if intent_match or domain_match:
                selected_clients.append(client_id)

        return selected_clients

    def _log_decision(self, decision: RoutingDecision):
        self.logger.info(
            "Routing decision made",
            extra={
                "decision": decision.dict(),
                "timestamp": datetime.utcnow().isoformat()
            }
        )

    def _generate_cache_key(self, analysis: Analysis, llm_context: Dict[str, Any] = None) -> str:
        """Generate a cache key based on analysis and context."""
        cache_data = {
            "intent": analysis.intent,
            "domains": sorted(analysis.domains),
            "confidence": analysis.confidence,
            "requires_decomposition": analysis.requires_decomposition,
            "context": llm_context or {}
        }
        
        # Create a stable JSON representation
        cache_str = json.dumps(cache_data, sort_keys=True)
        
        # Generate hash
        return hashlib.sha256(cache_str.encode()).hexdigest()

    async def _calculate_base_score(self, analysis: Analysis, rules: Dict[str, Any]) -> float:
        """Calculate base routing score based on analysis and rules."""
        base_score = 0.0
        
        # Check confidence threshold
        if analysis.confidence >= rules.get('min_confidence', 0.5):
            base_score += 0.5
            
        # Add domain-specific scoring
        if analysis.domains and set(analysis.domains).intersection(rules.get('supported_domains', [])):
            base_score += 0.3
            
        # Add intent-specific scoring
        if analysis.intent in rules.get('supported_intents', []):
            base_score += 0.2
            
        return base_score

    def _get_applied_rules(self, analysis: Analysis, rules: Dict[str, Any]) -> List[str]:
        """Retorna lista de regras aplicadas durante a análise."""
        applied_rules = []
        
        # Regra de confiança mínima
        if analysis.confidence >= rules.get('min_confidence', 0.5):
            applied_rules.append('min_confidence')
            
        # Regras de domínio
        if analysis.domains:
            for domain in analysis.domains:
                if domain in rules.get('supported_domains', []):
                    applied_rules.append(f'domain_{domain}')
                    
        # Regras de intenção
        if analysis.intent in rules.get('supported_intents', []):
            applied_rules.append(f'intent_{analysis.intent}')
            
        return applied_rules
