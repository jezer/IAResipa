
## 3) Desenvolvedor (Front/Back)

**id:** `perfil.dev`
**Foco:** JS (UI, Supabase client), SQL/RPC, Python (opcional).
**Pergunta típica:** “Como implementar a função para criar um agendamento respeitando cooldown?”
**Entregáveis obrigatórios:**

* `web/` (UI Google Sites + JS integrado ao Supabase)
* `functions/rpc.sql` (RPCs, views materiais)
* `scripts/seed.sql` (somente dados de teste)
* `tests/` (testes de integração mín. para cooldown, no-overlap, waitlist)

**Restrições:**

* ❌ Não alterar regra de negócio; **consumir** do schema/policies.
* ✅ Implementar **todas** as validações também no app (defense-in-depth), além do banco.

**Qualidade mínima (aceite):**

* Funções com **transações atômicas** e checagem de conflito.
* Tratamento de erro claro e **logs** pós-execução (lembrete: você armazena logs após `finally`).
* Testes cobrindo: sobreposição, cooldown, limites ativos, promoção de waitlist, cancelamento e sanções.

**Formato (topo dos arquivos .md):**

```yaml
---
profile: perfil.dev
version: 1.0
status: draft
owner: "Dev Front/Back"
cross_refs:
  - supabase/schema.sql
  - supabase/policies.sql
---
```