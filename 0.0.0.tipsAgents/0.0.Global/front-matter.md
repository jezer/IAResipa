**São Paulo — 18/08/2025 09:20**

## Minha recomendação (prática)

Para o seu cenário (RAG profundo, n8n/Databricks, múltiplos agentes e perfis especializados):

1. **Estruture por pastas (Opção 2)** para refletir áreas/times/domínios.
2. **Adote um `agents.yaml` na raiz (Opção 3)** como fonte canônica de políticas e donos, com **overrides por front-matter** só quando necessário.
3. Se o número de agentes e clientes crescer, **evolua para DB (Opção 4)** mantendo o `agents.yaml` como fallback/bootstrapping.

## Esboços (mínimos) para começar

**Front-matter por arquivo (override pontual):**

```md
---
agent: "quiosque.agendamento"
role: "Dev"
guardrails:
  scope: ["agendar", "lista_espera"]
  deny_out_of_scope: true
owners: ["@time-quiosques"]
embedding_namespace: "quiosque/agendamento"
---
```

**Manifesto raiz (`agents.yaml`):**

```yaml
defaults:
  guardrails:
    deny_out_of_scope: true
    pii_redaction: strict
  embedding:
    namespace: "global"
    chunk: {size: 800, overlap: 120}

profiles:
  - match: "quiosque/**"
    owners: ["@time-quiosques"]
    role: "Negocio"
    embedding: {namespace: "quiosque"}
  - match: "infra/**"
    owners: ["@arq-infra"]
    role: "Arquiteto"
    guardrails: {tools_allowed: ["supabase","n8n","databricks"]}
overrides:
  - match: "quiosque/familia/**"
    guardrails: {scope: ["quiosque_familia"]}
```

**Schema DB (Supabase) simplificado (Opção 4):**

```sql
create table agent_profiles(
  id uuid primary key default gen_random_uuid(),
  name text not null,
  match_glob text not null,
  role text not null,
  owners text[] not null,
  guardrails jsonb not null,
  embedding jsonb not null,
  version int not null default 1,
  active boolean not null default true,
  updated_at timestamptz not null default now()
);
```

**Resolver de políticas (ordem sugerida):**

1. Carrega `agents.yaml` (ou DB).
2. Aplica **match por pasta/glob** → herda `defaults`.
3. Aplica **overrides do manifesto**.
4. Se existir **front-matter no arquivo**, aplica por último.
5. Em CI: valida conflitos (ex.: owners divergentes, escopos incoerentes).

---

### TL;DR

* Poucos agentes/equipe pequena → **Opção 1** é ok.
* Crescimento e governança → **Opção 2 + 3** (pasta + manifesto) é o **mais produtivo**.
* Multi-produtos/tenants e operação 24x7 → **Opção 4** (registro em DB) fecha o ciclo com auditoria e toggles em tempo real.
