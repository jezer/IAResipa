# Atividade 5: Elaboração da Instrução (Prompt) para o Agente Coordenador

- [ ] **5.1. Redigir a Instrução de Forma Clara e Estruturada:**
    - [ ] A "instrução" (prompt ou sistema) a ser fornecida ao Gemini coordenador deve ser **clara, estruturada e abrangente**.
    - [ ] Utilizar **linguagem natural com bullet points ou passos numerados** para facilitar a leitura e compreensão pelo modelo.

- [ ] **5.2. Especificar o Papel e os Recursos Disponíveis:**
    - [ ] Iniciar definindo explicitamente o papel do agente (ex: "Você é um agente coordenador capaz de chamar outros 20 agentes especialistas.").
    - [ ] **Listar todos os agentes disponíveis e suas funções resumidamente** (ex: "Agentes disponíveis: [Pedido] cria novos pedidos; [Cancelamento] cancela pedidos existentes;").

- [ ] **5.3. Incluir Regras de Decisão Explícitas:**
    - [ ] Adicionar instruções claras sobre **como decidir qual agente chamar**, incluindo lógica para a primeira interação versus interações subsequentes.
    - [ ] Exemplificar com regras condicionais (ex: "se um pedido foi criado e o usuário pedir para cancelar, chame o agente de cancelamento.").

- [ ] **5.4. Orientar o Uso da Memória (Supabase):**
    - [ ] Instruir o agente coordenador a **sempre usar a memória de contexto do Supabase**.
    - [ ] Especificar tanto a **recuperação** ("Sempre que necessário, recupere do banco de dados (Supabase) informações relevantes do histórico") quanto a **atualização** ("Atualize o histórico no banco após cada ação bem-sucedida").

- [ ] **5.5. Definir o Formato da Saída (se aplicável):**
    - [ ] Se for necessário que o coordenador retorne um resultado estruturado para o sistema (não para o usuário), incluir um template na instrução (ex: `{"acao":"cancelar_pedido", "pedido_id":1234}`).
    - [ ] Alternativamente, instruir o LLM a focar em **ações** em vez de respostas em linguagem natural, especialmente se usando `function calling` nativa.

- [ ] **5.6. Realizar Testes e Refinamento Contínuo da Instrução:**
    - [ ] Testar diferentes formulações da instrução e **ajustar conforme o desempenho do LLM**.
    - [ ] Documentar a instrução em um formato fácil de atualizar (ex: arquivo YAML/JSON ou no próprio código) para facilitar a manutenção.
