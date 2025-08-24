# Atividade 3: Configuração e Uso da Memória de Contexto com Supabase

- [ ] **3.1. Designar Supabase como Repositório de Memória:**
    - [ ] Utilizar o **Supabase (que oferece um banco de dados PostgreSQL)** como o repositório principal para a **memória de longo prazo** do sistema.
    - [ ] Isso permitirá ao orquestrador **armazenar e recuperar informações de estado** para garantir a continuidade das interações.

- [ ] **3.2. Implementar Camadas de Memória no Supabase:**
    - [ ] **Histórico de Mensagens (Curto Prazo):** Gravar cada mensagem do usuário e resposta do sistema no Supabase para **recuperar o diálogo recente** e permitir que o coordenador veja ações anteriores (ex: "Pedido #123 criado no passo anterior").
    - [ ] **Memória Semântica (Opcional/Vetorial):** Opcionalmente, usar a **extensão `pgvector` do Supabase** para armazenar embeddings das interações, facilitando a busca semântica de informações mencionadas implicitamente (ex: "aquele produto que pedi mês passado").
    - [ ] **Memória Estruturada (Tabular):** Armazenar **dados estruturados relevantes em tabelas PostgreSQL** (ex: registros de pedidos com ID, item, status) para garantir precisão em consultas específicas (ex: "Qual o status do meu pedido #123?"). Esta memória estruturada permite que **múltiplos agentes consultem informações compartilhadas** eficientemente.

- [ ] **3.3. Definir a Interação do Coordenador com o Supabase:**
    - [ ] **Consulta Direta pelo Código:** A aplicação Python do coordenador deve **consultar o Supabase antes de chamar o Gemini**, buscando informações contextuais relevantes para incluir no prompt do modelo (ex: `Contexto: Pedido_atual_id=1234, status=CRIADO`).
    - [ ] **Função de Memória como Ferramenta (Alternativa):** Expor uma função/tool ao LLM (ex: `consultar_memoria(chave)`) para que o Gemini possa decidir chamar essa ferramenta quando precisar de detalhes do banco de dados.
    - [ ] **Atualização do Contexto Pós-Ação:** Sempre que um agente especializado executar uma ação, o coordenador deve **persistir os resultados ou mudanças de estado no Supabase** (ex: `ultima_acao="pedido_criado"`, `ultimo_pedido_id=1234`) para referência futura.
