

# 1) Princípios para alta assertividade

* **Fonte de verdade explícita (oracle):** defina exatamente *onde* validar (ex.: DB, API, log, PDF impresso, fila).
* **Dados determinísticos:** seeds fixas, IDs previsíveis, relógio congelado quando possível.
* **Pré-condições & fixtures:** como preparar ambiente/dados e como limpar (**teardown**).
* **Passos observáveis:** cada ação gera evidência colecionável (print de resposta, query, hash de arquivo, screenshot).
* **Critérios de aceite binários:** “passa/falha” objetivos; evite linguagem ambígua.
* **Coberturas:** funcional (caminhos felizes/erros), contratos, permissões, concorrência, idempotência, performance e segurança básica.
* **Reprodutibilidade:** todos os artefatos versionados (inputs, scripts, evidências).
* **Nomenclatura rastreável:** `TEST-<módulo>-<ação>-<variação>` e vincule a requisitos.

# 2) Prompt‐padrão para o agente gerar testes

> **Objetivo:** \[o que validar]
> **Sistema/Área:** \[módulo]
> **Escopo:** \[CRUD, impressão, auditoria…]
> **Oráculos:** \[fonte de validação]
> **Restrições:** \[limites de tempo, roles, integrações]
> **Ambiente:** \[dev/stage], *seed* = 4242, *clock*=“2025-08-24T10:00:00Z”
> **Métricas de assertividade:** taxa de falsos positivos/negativos, cobertura de caminhos críticos, consistência em 3 execuções.
> **Saídas exigidas:**
>
> 1. **Plano de teste** (tabela)
> 2. **Cenários Gherkin**
> 3. **Casos passo a passo com oráculos e evidências esperadas**
> 4. **Script de dados (setup/teardown)**
> 5. **Checklist de riscos/edge cases**
> 6. **Plano de regressão mínima**

# 3) Template de Plano de Teste (preenchível)

| Campo               | Conteúdo                                                             |
| ------------------- | -------------------------------------------------------------------- |
| ID / Nome           | TEST-PEDIDO-CRIAR-001                                                |
| Objetivo            | Validar criação, impressão e verificação do pedido                   |
| Escopo              | API `POST /pedidos`, geração de PDF, fila de impressão               |
| Fora do escopo      | Meios de pagamento externos                                          |
| Oráculos            | DB: `orders`, API: `GET /pedidos/{id}`, Arquivo: PDF hash            |
| Pré-condições       | Usuário `ROLE_VENDEDOR`, produto ativo, estoque ≥ 1                  |
| Dados               | Cliente X, Produto Y, Qty 2, Preço Z, Seed 4242                      |
| Ambiente            | STAGE, clock fixo                                                    |
| Riscos              | Race condition na numeração, impressora offline                      |
| Critérios de aceite | Status 201, registro no DB, PDF gerado, impressão confirmada         |
| Evidências          | JSON responses, SQL snapshots, hash SHA256 do PDF, log de impressora |
| Teardown            | Deletar pedido, limpar filas, remover arquivos temporários           |

# 4) Cenários em Gherkin (exemplos curtos)

**Criar e imprimir pedido (caminho feliz)**

```
Given usuário "ROLE_VENDEDOR" autenticado e produto "Y" com estoque 2
When criar um pedido com qty=2
Then a API retorna 201 e o corpo contém "pedidoId"
And no DB existe registro com "pedidoId" e status "CRIADO"
When solicitar impressão do pedidoId
Then um PDF é gerado e enviado à fila "IMPRESSORA_PADRAO"
And o hash do PDF corresponde ao esperado
```

**Deletar pedido (dependendo do fluxo de criação)**

```
Given um pedido válido foi criado (reuso do cenário "Criar e imprimir pedido")
When deletar o pedidoId
Then a API retorna 204
And uma consulta por pedidoId retorna "não existe"
And no DB o registro está ausente (ou marcado "DELETADO" conforme regra)
```

# 5) Caso de teste detalhado (passo a passo + oráculos)

**TC-PEDIDO-CREATE-PRINT-001**

1. **Setup:** inserir cliente/produto; clock=fixo; seed=4242.

   * *Evidência:* script de seed + confirmação por query.
2. **Criar pedido (POST /pedidos):** payload determinístico.

   * *Oráculo 1:* HTTP 201, schema válido.
   * *Oráculo 2:* `SELECT * FROM orders WHERE id=:pedidoId` → status=“CRIADO”.
3. **Imprimir:** `POST /pedidos/{id}/imprimir`.

   * *Oráculo 3:* arquivo PDF gerado; calcule **SHA256** e compare a esperado.
   * *Oráculo 4:* entrada na fila “IMPRESSORA\_PADRAO” com `jobId` e `pedidoId`.
4. **Teardown:** apagar pedido, limpar fila/arquivos.

   * *Oráculo 5:* `GET /pedidos/{id}` → 404 (se regra permite apagar) **ou** DB marcado “DELETADO”.

# 6) Variações e negativos obrigatórios

* **Validação de campos:** qty=0, produto inativo, cliente bloqueado.
* **Permissões:** tentar criar/imprimir com `ROLE_VISITANTE` → 403.
* **Idempotência:** repetir `POST` com mesmo idempotency-key → não duplicar.
* **Concorrência:** 5 criações simultâneas → numeração única.
* **Resiliência:** fila de impressão indisponível → erro claro + reprocesso.
* **Auditoria:** eventos “PEDIDO\_CRIADO/IMPRESSO/DELETADO” presentes.

# 7) Métricas de qualidade (o agente deve reportar)

* **Cobertura funcional dos requisitos críticos:** ≥ 90%.
* **Taxa de flakiness:** ≤ 2% em 3 execuções seguidas.
* **Tempo máximo por suíte:** p90 ≤ X min.
* **Evidências completas:** 100% dos passos com prova (log/SQL/PDF hash).
* **Defeitos por cenário:** acompanhar tendência e severidade.

# 8) Checklist rápido para cada teste

* [ ] Pré-condições claras e automatizadas
* [ ] Dados controlados (seed)
* [ ] Oráculos definidos para **cada** passo
* [ ] Evidências salvas com carimbo de tempo e IDs
* [ ] Teardown garante ambiente limpo
* [ ] Nomes e links para requisitos/usuário/regra

# 9) Exemplo de instrução ao agente (compacta)

> “Gere o **plano**, **cenários Gherkin**, **casos passo a passo**, **scripts de setup/teardown** e **lista de evidências** para:
> (A) Criar pedido → imprimir → validar impressão correta;
> (B) Deletar pedido (depende de A) → confirmar inexistência.
> Use seed=4242, clock fixo, roles explícitas, oráculos em API+DB+PDF hash+fila. Produza também 5 variações negativas, 2 testes de concorrência e 1 de idempotência.”
