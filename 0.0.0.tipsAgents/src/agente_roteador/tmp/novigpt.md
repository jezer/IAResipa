# Ajustes no desenho MCP

## 0) Princípios de roteamento

* **Fonte única de verdade**: o *Capability Registry* mora no MCP Server (nada de listas duplicadas nos clientes).
* **Roteamento = LLM + regras**: Gemini-Flash propõe intenções/capacidades; o Server valida contra o registry (score/threshold) e decide.
* **Fallback**: se nenhuma capacidade elegível ≥ *threshold*, o Server responde direto ao usuário (ou devolve “não suportado” com instruções/alternativas).

## 1) Registry de Capacidades (exemplo)

```yaml
# mcp_common/capabilities.yaml
clients:
  quality_agent:
    id: "quality_agent"
    match:
      intent: ["code_review","databricks_review","serverless_review"]
      domains: ["python","databricks","semaforo"]
    constraints:
      max_tokens: 8000
  rag_agent:
    id: "rag_agent"
    match:
      intent: ["retrieval_qa","doc_answering"]
      domains: ["kb_internal","docs"]
  billing_agent:
    id: "billing_agent"
    match:
      intent: ["cost_analysis"]
      domains: ["azure","databricks"]
routing:
  confidence_threshold: 0.65        # mínimo para aceitar sugestão do LLM
  topk: 2                           # no máx. 2 clientes por requisição
  conflict_policy: "prefer_specific" # empata? escolhe o mais específico
```

## 2) Prompt do Gemini-Flash (determinístico + JSON)

> **Meta**: sempre pedir **JSON estrito** com *intent*, *domains*, *subtasks* e *confidence*.

```text
SYSTEM
You are a router for a Multi-Agent MCP architecture. 
Return ONLY valid minified JSON (no commentary). 
Use the schema:
{
  "intent": "string",
  "domains": ["string"],
  "subtasks": [{"title":"string","reason":"string"}],
  "confidence": 0..1
}

CONTEXT
Capabilities registry (summary):
- quality_agent: intents {code_review, databricks_review, serverless_review}; domains {python, databricks, semaforo}
- rag_agent: intents {retrieval_qa, doc_answering}; domains {kb_internal, docs}
- billing_agent: intents {cost_analysis}; domains {azure, databricks}

USER_REQUEST
<<<
{texto_do_usuario}
>>>

CONSTRAINTS
- Classifique UMA intenção principal e 1-3 domínios.
- Se a tarefa for composta, divida em 1-3 subtarefas objetivas.
- Seja conservador: se não tiver confiança ≥0.5, reduza a abrangência.
```

### Validação do JSON (Pydantic)

* Se parsing falhar → **fallback**: heurísticas simples (palavras-chave) + “intent: unknown”.

## 3) Pipeline `handle_request` (resumo)

```python
async def handle_request(req: MCPRequest) -> MCPResponse:
    # 1) validar req
    payload = schemas.MCPRequest.parse_obj(req.dict())

    # 2) classificar com Gemini-Flash
    clf = await gemini_flash_classify(payload.content)

    # 3) decidir clientes
    candidates = match_candidates(clf, registry, threshold=cfg.routing.confidence_threshold)

    if not candidates:
        return await respond_fallback(payload, clf)  # ver seção 5

    # 4) particionar subtarefas (ou 1 tarefa única)
    tasks = task_manager.create_tasks(payload, candidates, clf.subtasks)

    # 5) despachar e monitorar
    await task_manager.dispatch(tasks)
    results = await task_manager.gather(tasks, timeout=cfg.server.task_timeout_seconds)

    # 6) agregar e responder
    return aggregate_response(payload.request_id, results)
```

### `match_candidates` (regras claras)

* **match score** = média ponderada:

  * +0.5 se `intent` ∈ intents do cliente
  * +0.3 por cada `domain` compatível (máx. +0.6)
  * −0.2 se violar `constraints`
* Filtra quem `score ≥ threshold` e mantém `topk`.

## 4) Contratos (sem ambiguidade)

* **Server → Clients (Task)**: inclui `intent`, `domains`, `subtask_title`, `inputs`, `trace_id`.
* **Clients → Server (Result)**: `status {success|failure|partial}`, `data`, `logs[]`, `metrics`, `explanations[]` (curtas, objetivas).

## 5) Fallback quando não há cliente elegível

Escolha 1 de 3 políticas (parametrizável):

**A. “Responder Direto” (default controlado)**

* Server usa Gemini-Flash para responder **no próprio Server** com *guardrails*:

  * Máx. tokens
  * Proibir ações fora de escopo (ex.: “não executo código”, “não altero infra”)
  * Citar que “não há agente especializado cadastrado para essa demanda”.

**B. “Não Suportado”**

* Resposta 4xx semântica: explica por que não há agente e sugere intents/domínios aceitos.

**C. “Propor Criação de Agente”**

* Abre ticket/registro no *AgenteCreator* com: exemplos de prompts, requisitos e riscos.

Exemplo rápido (A):

```python
async def respond_fallback(payload, clf):
    text = await gemini_flash_answer(
        question=payload.content.prompt,
        policy="safe_minimal",
        preamble="Não há agente especializado para essa demanda. Segue uma resposta direta e limitada:"
    )
    return MCPResponse(
        request_id=payload.request_id,
        status="completed",
        tasks=[],
        data={"mode":"server_fallback","classification":clf, "answer":text}
    )
```

## 6) Regras anti-surpresa (clareza)

* O Server **nunca** aciona cliente sem passar por `match_candidates`.
* Um cliente **nunca** reclassifica; ele só executa o que recebeu.
* Se o LLM sugerir múltiplos intents divergentes, o Server **divide** em subtarefas ou **pede clarificação** (política: `auto_split_if_conflict=True`).

## 7) Observabilidade específica do roteamento

* Logar: `request_id`, `clf.intent`, `clf.domains`, `clf.confidence`, `candidates[]`, `chosen[]`, `fallback_used`.
* Métricas: taxa de fallback, taxa de *misroute*, latência LLM, % de tasks com *partial*.

## 8) Segurança

* **LLM Boundary**: o Gemini-Flash só vê **estritamente** o necessário (prompt e metadados). Dados sensíveis mascarados.
* **Auth**: JWT entre clientes e server; escopos por agente.
* **Rate-limit** no endpoint de classificação e no fallback answer.

## 9) Tests focados no roteamento

* **Golden tests**: pares (input → cliente esperado).
* **Contract tests**: schemas válidos/inválidos.
* **Chaos**: simular `clf.confidence` baixo, JSON malformado, ausência de domínios.

---

### Snippet de integração (pseudo-SDK Gemini)

```python
async def gemini_flash_classify(content: dict) -> Classification:
    prompt = build_router_prompt(content["prompt"])
    raw = await gemini.generate(model="gemini-1.5-flash", input=prompt, json=True, max_tokens=300)
    return Classification.parse_raw(raw)

async def gemini_flash_answer(question: str, policy: str, preamble: str) -> str:
    sys = f"{preamble}\nResponda de forma breve, técnica e segura. Não invente capacidades."
    return await gemini.generate(model="gemini-1.5-flash", system=sys, input=question, max_tokens=600)
```

---

## Decisões que eliminam ambiguidade

* **Threshold explícito** (0.65) e **top-k** (2).
* **Política de empate**: “prefer\_specific” (cliente com mais *domains* compatíveis vence).
* **Fallback documentado** (A/B/C) e configurável.
* **JSON estrito** no roteador (sem texto extra).
* **Clientes jamais se falam entre si**.
