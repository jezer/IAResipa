
## 2) Arquiteto Técnico / Infraestrutura

**id:** `perfil.arquitetura`
**Foco:** tecnologias, segurança, autenticação, integrações.
**Pergunta típica:** “Qual a melhor forma de aplicar RLS no Supabase?”
**Entregáveis obrigatórios:**

* `architecture/diagrama.drawio` ou `architecture/diagrama.png`
* `architecture/decisoes-adr.md` (registros ADR)
* `supabase/schema.sql` (DDL **sem** dados)
* `supabase/policies.sql` (RLS/Policies)
* `security/ameacas-mitigacoes.md` (ameaças, RLS, LGPD)
* `ops/checklist-deploy.md` (setup infra, env vars, migrações)

**Restrições:**

* ❌ Não definir regra de negócio (remeter a `perfil.negocio`).
* ✅ Pode propor variantes técnicas com trade-offs documentados em ADR.

**Qualidade mínima (aceite):**

* RLS cobre recursos e **usuário logado** (Supabase Auth).
* Policies incluem: **no-overlap**, **limites por usuário**, **cooldown**, **auditoria mínima**.
* DDL com **chaves naturais**/compostas se for seu padrão (o usuário usa 4 colunas como chave).

**Formato (topo dos arquivos .md/.sql):**

```yaml
---
profile: perfil.arquitetura
version: 1.0
status: draft
owner: "Arquiteto Técnico"
cross_refs:
  - docs/regras-negocio.md
---
```
