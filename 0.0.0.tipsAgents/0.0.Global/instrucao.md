
Cada perfil tem:

* **ID único**
* **Escopo permitido**
* **Entregáveis obrigatórios**
* **Restrições e proibições**
* **Qualidade mínima (aceite)**
* **Vocabulário/tons aceitos**
* **Formato de saída** (com front-matter YAML para auditoria)

## 0) Padrões Globais (valem para todos)

* **Separação dura de perfis:** nunca responder fora do escopo do perfil ativo.
* **Parâmetros do negócio sempre parametrizáveis** (ex.: `cooldown_dias`, `antecedencia_min_horas`, etc.).
* **Nada de “achar” regras:** se não houver regra, documente como “Não definido” e **proponha** opções em anexo, sem assumir valor.
* **Citações cruzadas:** um perfil pode **referenciar** outro apenas via link/ID do entregável, **sem reescrever** conteúdo do outro perfil.
* **Formatos aceitos:** `.md` para docs, `.sql`/`.js`/`.py` para código, `.png/.drawio` para diagramas.
