# Atividade 4: Desenvolver o Fluxo de Execução e Lógica de Seleção do Agente Coordenador

- [ ] **4.1. Receber e Registrar a Solicitação do Usuário:**
    - [ ] O sistema deve capturar a solicitação do usuário (ex: "Quero fazer um pedido do produto X") e entregá-la ao agente coordenador (Gemini), juntamente com a instrução do sistema e o contexto prévio (se houver).

- [ ] **4.2. Analisar o Tipo de Solicitação e Roteamento Inicial:**
    - [ ] **Primeira Interação:** Se for a primeira ordem da conversa, o coordenador deve **identificar a intenção do usuário para escolher o agente especialista apropriado** (ex: "fazer um pedido" -> AgenteDePedido). O LLM pode usar seu **raciocínio lógico e planejamento** para quebrar a tarefa e planejar a primeira etapa.
    - [ ] **Interações Subsequentes:** Se não for a primeira interação, o coordenador precisa **consultar o Supabase para recuperar informações relevantes do histórico** (ex: ID do último pedido) para entender o estado atual e o que o usuário está referenciando.

- [ ] **4.3. Selecionar o Agente Apropriado para a Nova Solicitação:**
    - [ ] Com a intenção do usuário e o contexto identificados, o coordenador **escolherá qual agente chamar em seguida** (ex: após criar um pedido, "cancelar o pedido" será roteado para o AgenteDeCancelamento).
    - [ ] A decisão pode ser baseada na instrução do coordenador ou ser decidida dinamicamente pelo LLM, que pode ser instruído a retornar uma **saída estruturada** (ex: JSON com `next_agent`) para facilitar o roteamento programático.

- [ ] **4.4. Refinar a Instrução e Chamar o Agente Especialista:**
    - [ ] Antes de invocar o agente escolhido, o coordenador pode **complementar a solicitação com dados de contexto** (ex: inserir o ID do pedido na requisição de cancelamento) e formatar a ordem de forma estruturada para o agente.
    - [ ] A chamada ao agente pode ser feita via **`function call` nativa do LLM** (se usando Gemini) ou por requisição HTTP via o código do coordenador.

- [ ] **4.5. Receber o Resultado e Registrar Mudanças:**
    - [ ] O coordenador deve receber a resposta do agente especializado (ex: "Pedido 1234 criado com sucesso").
    - [ ] É **vital registrar o resultado no Supabase**, atualizando a memória com o novo estado para referência futura.

- [ ] **4.6. Iterar e Habilitar Colaboração Multi-Agente:**
    - [ ] O processo deve se repetir a cada nova entrada do usuário, permitindo **fluxos multi-passos complexos e vários agentes colaborando em sequência**.
    - [ ] O coordenador atuará como **gerente de fluxo**, garantindo que o output de um agente sirva como input para o próximo (encadeamento). A memória compartilhada no Supabase é crucial para este encadeamento.
