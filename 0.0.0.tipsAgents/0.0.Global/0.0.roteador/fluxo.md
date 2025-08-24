

# 8) Fluxo operacional (Mermaid)

```mermaid
flowchart TD
A[Usuário envia prompt] --> B{AgenteRoteador<br/>detectar intent/domínio}
B -->|1 assunto| C[Encaminha p/ 1 agente alvo]
B -->|2+ assuntos| D[Split do prompt<br/>(partes por domínio)]
B -->|nenhum agente cobre| E[Rejeitar + sugerir AgenteCreator]

C --> F[Agente alvo responde]
D --> G[Executa cada parte em seu agente]
F --> H[Resposta ao usuário]
G --> H[Combina respostas e entrega]

E --> I[Opcional: abrir requisição p/ AgenteCreator]

subgraph Diária 03:00
J[AgenteQualidade] --> K[Coleta logs & artefatos]
K --> L[KPIs, clusters, conflitos]
L --> M[PRs automáticos nos agents]
M --> N[Rodar lint & checklists]
N --> O[Publica relatório e aplica melhorias]
end
```