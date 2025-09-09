# Plano de Implementação da Arquitetura MCP (Model Context Protocol)

*Nota: O termo "Model Context Protocol" parece ser uma definição específica para este projeto. Recomendo adicionar um pequeno glossário no início ou em um documento complementar para definir formalmente este e outros termos-chave, garantindo que todos os envolvidos compartilhem o mesmo entendimento.*

Este documento detalha as instruções passo a passo para transformar o sistema atual em uma arquitetura MCP, onde o `agente_roteador` atua como **MCP Server** e os agentes especializados como **MCP Clients**.

## Definições Importantes

### MCP Server (Agente Roteador)
- Ponto central de recebimento de solicitações.
- Orquestrador da comunicação e do ciclo de vida das tarefas.
- Responsável pelo roteamento, monitoramento e agregação de resultados.

### MCP Clients (Agentes Especializados)
- Implementam um conjunto bem definido de capacidades.
- Processam tarefas de forma isolada e independente.
- Comunicam-se exclusivamente com o MCP Server via um contrato de API definido.

## Sequência de Implementação

1. **Estrutura de Diretórios MCP**
   *Sugestão: A estrutura proposta é excelente. A separação de `mcp_server`, `mcp_common`, e `mcp_clients` cria um baixo acoplamento e alta coesão.*
   ```
   agente_roteador/
   ├── mcp_server/
   │   ├── __init__.py
   │   ├── server.py           # Implementação do servidor (ex: FastAPI, gRPC)
   │   ├── router.py           # Lógica de roteamento de alto nível
   │   └── task_manager.py     # Gerenciamento do ciclo de vida das tarefas
   ├── mcp_common/
   │   ├── __init__.py
   │   ├── models.py           # Modelos de dados compartilhados (Pydantic, dataclasses)
   │   ├── schemas/            # Schemas JSON para validação de mensagens
   │   └── base_client.py      # Classe base abstrata para clientes
   └── mcp_clients/
       └── __init__.py         # Registry dinâmico de clientes disponíveis
   ```

2. **Implementação do MCP Server com Gemini Integration**

   a. **Componente de Análise com Gemini**
   ```python
   class GeminiAnalyzer:
       def __init__(self, model_config: Dict[str, Any]):
           self.model = genai.GenerativeModel('gemini-pro')
           self.context_template = self._load_context_template()

       async def analyze_request(self, content: str) -> List[MCPActivity]:
           prompt = f"""
           Analise a seguinte solicitação e divida em atividades distintas.
           Para cada atividade, identifique:
           1. Descrição clara e objetiva
           2. Capacidades técnicas necessárias
           3. Dependências (se houver)
           4. Prioridade sugerida (1-5)

           Formato JSON esperado:
           {{
             "activities": [
               {{
                 "description": "descrição da atividade",
                 "required_capabilities": ["cap1", "cap2"],
                 "dependencies": ["id_atividade_anterior"],
                 "priority": número,
                 "estimated_complexity": "low|medium|high"
               }}
             ]
           }}

           Solicitação: {content}
           """
           
           try:
               response = await self.model.generate_content_async(prompt)
               activities = json.loads(response.text)
               return self._validate_and_structure_activities(activities)
           except Exception as e:
               logging.error(f"Erro na análise Gemini: {str(e)}")
               raise MCPAnalysisError("Falha na análise da solicitação")
   ```

   b. **Implementação do MCP Server com Gemini**
   ```python
   class MCPServer:
       def __init__(self):
           self.router = TaskRouter()
           self.task_manager = TaskManager()
           self.client_registry = ClientRegistry()
           self.gemini_analyzer = GeminiAnalyzer(config.gemini)
           self.capability_matcher = CapabilityMatcher()

       async def handle_request(self, request: MCPRequest) -> MCPResponse:
           try:
               # 1. Análise da solicitação com Gemini
               activities = await self.gemini_analyzer.analyze_request(request.content)

               # 2. Matching de atividades com clientes disponíveis
               assignments = []
               unmatched = []

               for activity in activities:
                   client = self.capability_matcher.find_best_client(
                       activity.required_capabilities
                   )
                   
                   if client:
                       assignments.append(MCPAssignment(
                           activity=activity,
                           client=client,
                           priority=activity.priority
                       ))
                   else:
                       unmatched.append(activity)

               # 3. Se houver atividades sem match, prepara resposta apropriada
               if unmatched:
                   return self._create_unmatched_response(
                       request.request_id,
                       assignments,
                       unmatched
                   )

               # 4. Criar e distribuir tarefas para atividades com match
               tasks = await self.task_manager.create_tasks(assignments)
               
               # 5. Retornar resposta com status das tarefas
               return MCPResponse(
                   request_id=request.request_id,
                   status="accepted",
                   tasks=tasks
               )

           except Exception as e:
               logging.error(f"Erro no processamento: {str(e)}")
               return self._create_error_response(request.request_id, str(e))

       def _create_unmatched_response(
           self,
           request_id: str,
           matched: List[MCPAssignment],
           unmatched: List[MCPActivity]
       ) -> MCPResponse:
           """Cria resposta detalhada para atividades sem agentes correspondentes"""
           
           # Agrupa capacidades faltantes para sugestão de novos agentes
           missing_capabilities = set()
           for activity in unmatched:
               missing_capabilities.update(activity.required_capabilities)

           return MCPResponse(
               request_id=request_id,
               status="partial" if matched else "rejected",
               tasks=[a.to_task() for a in matched] if matched else [],
               unmatched_activities=[{
                   "description": act.description,
                   "required_capabilities": act.required_capabilities,
                   "reason": "Não há agente disponível com as capacidades necessárias"
               } for act in unmatched],
               suggestion={
                   "type": "new_agents_needed",
                   "missing_capabilities": list(missing_capabilities),
                   "recommended_action": "Considere criar novos agentes com estas capacidades"
               }
           )
   ```

   c. **Capability Matcher para Análise Precisa**
   ```python
   class CapabilityMatcher:
       def __init__(self):
           self.capability_embeddings = {}
           self.threshold = 0.75  # Limiar de confiança para match

       def find_best_client(
           self,
           required_capabilities: List[str]
       ) -> Optional[MCPClient]:
           """
           Encontra o melhor cliente que atenda às capacidades requeridas
           usando matching semântico e exato
           """
           best_match = None
           best_score = 0

           for client in self.registered_clients:
               score = self._calculate_capability_match(
                   required_capabilities,
                   client.capabilities
               )
               
               if score > best_score and score >= self.threshold:
                   best_match = client
                   best_score = score

           return best_match
   ```

3. **Definição do Base Client**
   ```python
   from abc import ABC, abstractmethod

   class BaseMCPClient(ABC):
       def __init__(self):
           self.capabilities = self.load_capabilities()
           self.task_queue = asyncio.Queue()

       @abstractmethod
       async def handle_task(self, task: MCPTask) -> MCPResult:
           # Template method para ser implementado por cada cliente
           pass

       async def report_status(self, task_id: str, status: TaskStatus):
           # Reporta progresso, sucesso ou falha ao TaskManager do servidor
           pass
   ```

4. **Protocolos de Comunicação MCP com Suporte a Atividades Não Atendidas**
   *Sugestão: Estes schemas são a parte mais crítica do protocolo. Inclui suporte para reportar atividades que não podem ser atendidas e sugestões de novos agentes.*

   a. **Schema de Requisição (Cliente -> Servidor)**
   ```json
   {
     "MCPRequest": {
       "request_id": "UUID",
       "timestamp": "ISO8601",
       "type": "task|query|control",
       "content": {
         "prompt": "texto da solicitação",
         "parameters": {},
         "context": {}
       }
     }
   }
   ```

   b. **Schema de Resposta Estendido (Servidor -> Cliente)**
   ```json
   {
     "MCPResponse": {
       "request_id": "UUID",
       "timestamp": "ISO8601",
       "status": "accepted|partial|rejected|completed",
       "tasks": [{
         "task_id": "UUID",
         "assigned_agent": "agent_id",
         "priority": 1,
         "status": "pending|running|completed|failed"
       }],
       "unmatched_activities": [{
         "description": "descrição da atividade não atendida",
         "required_capabilities": ["cap1", "cap2"],
         "reason": "explicação detalhada do motivo"
       }],
       "suggestion": {
         "type": "new_agents_needed|alternative_approach",
         "missing_capabilities": ["lista de capacidades faltantes"],
         "recommended_action": "sugestão para resolver o problema"
       }
     }
   }
   ```

   c. **Schema de Resultado da Tarefa (Cliente -> Servidor)**
   ```json
   {
     "MCPTaskResult": {
       "task_id": "UUID",
       "agent_id": "string",
       "status": "success|failure|partial",
       "result": {},
       "error_details": "se status for failure",
       "metrics": {
         "start_time": "ISO8601",
         "end_time": "ISO8601",
         "processing_time_ms": 1000
       }
     }
   }
   ```

5. **Implementação dos Modelos e Configuração**
   *Sugestão de Melhoria: Centralizar a configuração em uma única classe ou objeto que possa ser injetado onde for necessário (Dependency Injection). Isso facilita o gerenciamento em diferentes ambientes (dev, prod).*
   
   a. **Modelos Base (mcp_common/models.py)**
   ```python
   @dataclass
   class MCPAgent:
       id: str
       type: str
       capabilities: List[str]
       status: str # (e.g., online, offline, busy)
       metrics: Dict[str, Any]

   @dataclass
   class MCPTask:
       id: str
       type: str
       priority: int
       content: Any
       metadata: Dict[str, Any]
       dependencies: List[str]
   ```

   b. **Configuração Centralizada (config.yaml)**
   ```yaml
   mcp_server:
     host: "localhost"
     port: 5000
     max_concurrent_tasks: 100
     task_timeout_seconds: 300

   mcp_clients_defaults:
     reconnect_attempts: 3
     heartbeat_interval_seconds: 30
     task_queue_size: 50
   
   logging:
      level: "INFO"
      format: "json"
   ```

6. **Adaptação dos Componentes Existentes**
   *Ótima abordagem. Os componentes existentes se tornam serviços internos do MCP Server, promovendo a reutilização.*
   ```python
   class MCPRouter(MCPService):
       # ... (como definido anteriormente)

   class MCPTaskAnalyzer(MCPService):
       # ... (como definido anteriormente)
   ```

7. **Sistema de Observabilidade MCP**
   *Excelente seção. O rastreamento distribuído é crucial para a depuração.*
   ```python
   # ... (como definido anteriormente, a estrutura está muito boa)
   ```

8. **Implementação de Clientes MCP**
   *Exemplo claro e direto.*
   ```python
   class QualityAgentClient(BaseMCPClient):
       # ... (como definido anteriormente)
   ```

9. **Testes e Validação**
   *Sugestão: Adicionar testes de contrato, que verifiquem se os clientes e o servidor estão aderindo aos schemas de comunicação definidos.*

10. **Documentação e Manutenção**
    *Perfeito.*

11. **Próximos Passos e Considerações de Segurança**
    *Excelente visão de futuro. Adicionaria "Estratégia de Tratamento de Erros" como um subtópico, detalhando políticas de retry, dead-letter queues para tarefas que falham consistentemente, e como os erros são comunicados ao solicitante original.*
