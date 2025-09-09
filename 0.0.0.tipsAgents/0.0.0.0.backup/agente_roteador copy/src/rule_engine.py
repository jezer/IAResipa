import re
from typing import List, Dict, Any, Tuple
from models import Task, AgentConfig

class RuleEngine:
    def __init__(self, available_agents: List[AgentConfig]):
        self.available_agents = {agent.id: agent for agent in available_agents}
        self.keyword_patterns = self._compile_patterns()

    def _compile_patterns(self) -> Dict[str, List[Tuple[re.Pattern, str]]]:
        """
        Compila os padrões de regex para cada agente baseado em suas capacidades
        """
        patterns = {}
        
        # Padrões para o agente_creator
        patterns["agente_creator"] = [
            (re.compile(r'\b(criar|novo|desenvolver)\s+agente\b', re.I), "Solicitação de criação de agente"),
            (re.compile(r'\b(nova|adicionar)\s+capacidade\b', re.I), "Adição de nova capacidade")
        ]
        
        # Padrões para o agente_quality
        patterns["agente_quality"] = [
            (re.compile(r'\b(analis[ae][rs]?|verific[ae][rs]?)\s+(qualidade|consistência|conformidade)\b', re.I), 
             "Análise de qualidade"),
            (re.compile(r'\b(audit[ae][rs]?|avaliar)\b', re.I), "Auditoria de sistema")
        ]
        
        # Padrões para o agente_fluxos
        patterns["agente_fluxos"] = [
            (re.compile(r'\b(fluxo|diagrama|visualiz[ae][rs]?|map[ae][rs]?)\b', re.I), 
             "Criação de diagrama ou fluxo"),
            (re.compile(r'\b(document[ae][rs]?)\s+(processo|fluxo)\b', re.I), 
             "Documentação de processo")
        ]
        
        # Padrões para o agente_implementador
        patterns["agente_implementador"] = [
            (re.compile(r'\b(implement[ae][rs]?|desenvolver|codific[ae][rs]?)\b', re.I), 
             "Implementação de código"),
            (re.compile(r'\b(criar|desenvolver)\s+(função|módulo|recurso)\b', re.I), 
             "Desenvolvimento de funcionalidade")
        ]
        
        return patterns

    def analyze_request(self, content: str) -> List[Task]:
        """
        Analisa uma solicitação e retorna as tarefas identificadas em ordem de prioridade
        """
        matches = []
        
        for agent_id, patterns in self.keyword_patterns.items():
            agent = self.available_agents[agent_id]
            
            for pattern, reason in patterns:
                if pattern.search(content):
                    confidence = self._calculate_confidence(content, pattern)
                    matches.append({
                        "agent_id": agent_id,
                        "priority": agent.priority,
                        "confidence": confidence,
                        "reason": reason,
                        "pattern": pattern.pattern
                    })
        
        # Ordena por prioridade e confiança
        matches.sort(key=lambda x: (-x["priority"], -x["confidence"]))
        
        tasks = []
        for idx, match in enumerate(matches, 1):
            task = Task(
                sequence=idx,
                target_agent=match["agent_id"],
                priority=match["priority"],
                content=content,
                reasoning={
                    "matched_criteria": [match["pattern"]],
                    "confidence": match["confidence"],
                    "reason": match["reason"]
                }
            )
            tasks.append(task)
        
        return tasks

    def _calculate_confidence(self, content: str, pattern: re.Pattern) -> float:
        """
        Calcula um score de confiança baseado na quantidade e qualidade dos matches
        """
        matches = pattern.findall(content.lower())
        if not matches:
            return 0.0
            
        # Base confidence from match existence
        confidence = 0.6
        
        # Boost for multiple matches
        confidence += min(len(matches) * 0.1, 0.2)
        
        # Boost for match position (higher if appears early in content)
        first_match_pos = content.lower().find(matches[0])
        if first_match_pos < len(content) / 3:
            confidence += 0.1
            
        # Boost for context words
        context_boosts = {
            "por favor": 0.05,
            "preciso": 0.05,
            "necessito": 0.05,
            "importante": 0.05
        }
        
        for context, boost in context_boosts.items():
            if context in content.lower():
                confidence += boost
                
        return min(confidence, 0.95)  # Cap at 0.95

    def should_split_task(self, content: str, matches: List[Dict]) -> bool:
        """
        Determina se uma tarefa deve ser dividida baseado em critérios específicos
        """
        if len(matches) <= 1:
            return False
            
        # Verifica se há conectivos que indicam múltiplas tarefas
        split_indicators = [
            r'\be\b', r'\bdepois\b', r'\bem seguida\b', r'\btambém\b',
            r'\badicional(mente)?\b', r'\bfinalmente\b'
        ]
        
        for indicator in split_indicators:
            if re.search(indicator, content, re.I):
                return True
                
        # Verifica se há verbos diferentes para diferentes agentes
        verb_patterns = {
            "agente_creator": r'\b(criar|desenvolver)\b',
            "agente_quality": r'\b(analisar|verificar)\b',
            "agente_fluxos": r'\b(documentar|mapear)\b',
            "agente_implementador": r'\b(implementar|codificar)\b'
        }
        
        verb_count = sum(1 for pattern in verb_patterns.values() 
                        if re.search(pattern, content, re.I))
                        
        return verb_count > 1
