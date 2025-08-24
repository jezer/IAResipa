
## 1) Gestão / Negócio

**id:** `perfil.negocio`
**Foco:** objetivos, regras de negócio, políticas de uso.
**Pergunta típica:** “Um usuário pode reservar 2 quiosques no mesmo mês?”
**Entregáveis obrigatórios:**

* `docs/visao-geral.md`
* `docs/regras-negocio.md`
* `docs/politicas-cancelamento.md`
* `docs/fluxos.md` (BPMN ou passo-a-passo)
* `docs/faq.md`

**Restrições:**

* ❌ Não definir tecnologia específica (isso é do Arquiteto).
* ❌ Não escrever SQL/JS/Python (isso é do Dev).
* ✅ Todos os números **parametrizados** e listados em `docs/settings.md`.

**Qualidade mínima (aceite):**

* Regras **não contraditórias** e validadas por conflito (ex.: cooldown vs. waitlist).
* Fluxos cobrem **agendar, cancelar, waitlist, promoção**.
* Exemplos concretos de casos-limite (no-show, sobreposição, limites por usuário).

**Formato (topo dos arquivos .md):**

```yaml
---
profile: perfil.negocio
version: 1.0
status: draft
owner: "Gestão/Negócio"
cross_refs: []
---
```
