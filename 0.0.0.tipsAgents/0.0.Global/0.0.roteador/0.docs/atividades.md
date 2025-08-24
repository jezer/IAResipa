
### Plano de Atividades para Orquestração de Múltiplos Agentes de IA

Este plano descreve as etapas para a implementação de um sistema de agentes de IA coordenado por um Agente Orquestrador (baseado no Gemini), utilizando o Supabase para memória de contexto e permitindo a fácil adição de novos agentes.

---

**Atividade 1: Design e Definição da Arquitetura Multi-Agente**

1.  **1.1. Definir o Papel do Agente Coordenador:**
    *   Estabelecer um **Agente Coordenador central**, preferencialmente um **LLM (Large Language Model) como o Google Gemini**, que atuará como o "cérebro" do sistema.
    *   Este coordenador será responsável por interpretar as instruções do usuário, consultar o contexto armazenado e **decidir qual agente especializado chamar** para cada solicitação.
    *   Compreender que o coordenador seguirá o padrão de **"Coordenador/Dispatcher"**, roteando pedidos para agentes especialistas.

2.  **1.2. Identificar e Conceituar Agentes Especializados:**
    *   Dividir a aplicação em **múltiplos agentes especializados**, cada um focado em uma única função específica (por exemplo, "criar pedido", "cancelar pedido", "verificar estoque", "agente de pagamento", "agente de suporte técnico").
    *   Planejar a capacidade de ter **cerca de 20 (ou mais) agentes especializados**, à medida que o sistema cresce.

**Atividade 2: Implementação dos Agentes Especializados**

1.  **2.1. Codificar Cada Agente como Funções/Microserviços Independentes:**
    *   Implementar cada agente como uma **função ou microserviço Python independente**.
    *   Expor esses agentes via API, utilizando ferramentas como **endpoints REST em FastAPI** ou **funções serverless no Azure Functions**.
    *   Garantir que a **interface de cada agente seja bem definida** com inputs e outputs conhecidos para uma coordenação confiável.

2.  **2.2. Habilitar 'Function Calling' para o Gemini:**
    *   Aproveitar o recurso de `function calling` do Gemini, definindo cada agente especializado como uma "**função**" disponível para o modelo coordenador.
    *   Fornecer ao Gemini as **assinaturas e descrições dessas funções** (por exemplo, `criar_pedido(pedido_dados)`, `cancelar_pedido(pedido_id)`) para que ele possa escolher autonomamente a função correta.

3.  **2.3. Criar Descrições Claras para Cada Agente:**
    *   Elaborar **descrições claras e padronizadas** para cada agente, explicando sua função (ex: "Agente de Cobrança: lida com questões de pagamento"; "Agente de Suporte: resolve problemas técnicos").
    *   Essas descrições são **fundamentais para ajudar o coordenador** (LLM ou lógica customizada) a decidir corretamente qual agente chamar.

**Atividade 3: Configuração e Uso da Memória de Contexto com Supabase**

1.  **3.1. Designar Supabase como Repositório de Memória:**
    *   Utilizar o **Supabase (que oferece um banco de dados PostgreSQL)** como o repositório principal para a **memória de longo prazo** do sistema.
    *   Isso permitirá ao orquestrador **armazenar e recuperar informações de estado** para garantir a continuidade das interações.

2.  **3.2. Implementar Camadas de Memória no Supabase:**
    *   **Histórico de Mensagens (Curto Prazo):** Gravar cada mensagem do usuário e resposta do sistema no Supabase para **recuperar o diálogo recente** e permitir que o coordenador veja ações anteriores (ex: "Pedido #123 criado no passo anterior").
    *   **Memória Semântica (Opcional/Vetorial):** Opcionalmente, usar a **extensão `pgvector` do Supabase** para armazenar embeddings das interações, facilitando a busca semântica de informações mencionadas implicitamente (ex: "aquele produto que pedi mês passado").
    *   **Memória Estruturada (Tabular):** Armazenar **dados estruturados relevantes em tabelas PostgreSQL** (ex: registros de pedidos com ID, item, status) para garantir precisão em consultas específicas (ex: "Qual o status do meu pedido #123?"). Esta memória estruturada permite que **múltiplos agentes consultem informações compartilhadas** eficientemente.

3.  **3.3. Definir a Interação do Coordenador com o Supabase:**
    *   **Consulta Direta pelo Código:** A aplicação Python do coordenador deve **consultar o Supabase antes de chamar o Gemini**, buscando informações contextuais relevantes para incluir no prompt do modelo (ex: `Contexto: Pedido_atual_id=1234, status=CRIADO`).
    *   **Função de Memória como Ferramenta (Alternativa):** Expor uma função/tool ao LLM (ex: `consultar_memoria(chave)`) para que o Gemini possa decidir chamar essa ferramenta quando precisar de detalhes do banco de dados.
    *   **Atualização do Contexto Pós-Ação:** Sempre que um agente especializado executar uma ação, o coordenador deve **persistir os resultados ou mudanças de estado no Supabase** (ex: `ultima_acao="pedido_criado"`, `ultimo_pedido_id=1234`) para referência futura.

**Atividade 4: Desenvolver o Fluxo de Execução e Lógica de Seleção do Agente Coordenador**

1.  **4.1. Receber e Registrar a Solicitação do Usuário:**
    *   O sistema deve capturar a solicitação do usuário (ex: "Quero fazer um pedido do produto X") e entregá-la ao agente coordenador (Gemini), juntamente com a instrução do sistema e o contexto prévio (se houver).

2.  **4.2. Analisar o Tipo de Solicitação e Roteamento Inicial:**
    *   **Primeira Interação:** Se for a primeira ordem da conversa, o coordenador deve **identificar a intenção do usuário para escolher o agente especialista apropriado** (ex: "fazer um pedido" -> AgenteDePedido). O LLM pode usar seu **raciocínio lógico e planejamento** para quebrar a tarefa e planejar a primeira etapa.
    *   **Interações Subsequentes:** Se não for a primeira interação, o coordenador precisa **consultar o Supabase para recuperar informações relevantes do histórico** (ex: ID do último pedido) para entender o estado atual e o que o usuário está referenciando.

3.  **4.3. Selecionar o Agente Apropriado para a Nova Solicitação:**
    *   Com a intenção do usuário e o contexto identificados, o coordenador **escolherá qual agente chamar em seguida** (ex: após criar um pedido, "cancelar o pedido" será roteado para o AgenteDeCancelamento).
    *   A decisão pode ser baseada na instrução do coordenador ou ser decidida dinamicamente pelo LLM, que pode ser instruído a retornar uma **saída estruturada** (ex: JSON com `next_agent`) para facilitar o roteamento programático.

4.  **4.4. Refinar a Instrução e Chamar o Agente Especialista:**
    *   Antes de invocar o agente escolhido, o coordenador pode **complementar a solicitação com dados de contexto** (ex: inserir o ID do pedido na requisição de cancelamento) e formatar a ordem de forma estruturada para o agente.
    *   A chamada ao agente pode ser feita via **`function call` nativa do LLM** (se usando Gemini) ou por requisição HTTP via o código do coordenador.

5.  **4.5. Receber o Resultado e Registrar Mudanças:**
    *   O coordenador deve receber a resposta do agente especializado (ex: "Pedido 1234 criado com sucesso").
    *   É **vital registrar o resultado no Supabase**, atualizando a memória com o novo estado para referência futura.

6.  **4.6. Iterar e Habilitar Colaboração Multi-Agente:**
    *   O processo deve se repetir a cada nova entrada do usuário, permitindo **fluxos multi-passos complexos e vários agentes colaborando em sequência**.
    *   O coordenador atuará como **gerente de fluxo**, garantindo que o output de um agente sirva como input para o próximo (encadeamento). A memória compartilhada no Supabase é crucial para este encadeamento.

**Atividade 5: Elaboração da Instrução (Prompt) para o Agente Coordenador**

1.  **5.1. Redigir a Instrução de Forma Clara e Estruturada:**
    *   A "instrução" (prompt ou sistema) a ser fornecida ao Gemini coordenador deve ser **clara, estruturada e abrangente**.
    *   Utilizar **linguagem natural com bullet points ou passos numerados** para facilitar a leitura e compreensão pelo modelo.

2.  **5.2. Especificar o Papel e os Recursos Disponíveis:**
    *   Iniciar definindo explicitamente o papel do agente (ex: "Você é um agente coordenador capaz de chamar outros 20 agentes especialistas.").
    *   **Listar todos os agentes disponíveis e suas funções resumidamente** (ex: "Agentes disponíveis: [Pedido] cria novos pedidos; [Cancelamento] cancela pedidos existentes;").

3.  **5.3. Incluir Regras de Decisão Explícitas:**
    *   Adicionar instruções claras sobre **como decidir qual agente chamar**, incluindo lógica para a primeira interação versus interações subsequentes.
    *   Exemplificar com regras condicionais (ex: "se um pedido foi criado e o usuário pedir para cancelar, chame o agente de cancelamento.").

4.  **5.4. Orientar o Uso da Memória (Supabase):**
    *   Instruir o agente coordenador a **sempre usar a memória de contexto do Supabase**.
    *   Especificar tanto a **recuperação** ("Sempre que necessário, recupere do banco de dados (Supabase) informações relevantes do histórico") quanto a **atualização** ("Atualize o histórico no banco após cada ação bem-sucedida").

5.  **5.5. Definir o Formato da Saída (se aplicável):**
    *   Se for necessário que o coordenador retorne um resultado estruturado para o sistema (não para o usuário), incluir um template na instrução (ex: `{"acao":"cancelar_pedido", "pedido_id":1234}`).
    *   Alternativamente, instruir o LLM a focar em **ações** em vez de respostas em linguagem natural, especialmente se usando `function calling` nativa.

6.  **5.6. Realizar Testes e Refinamento Contínuo da Instrução:**
    *   Testar diferentes formulações da instrução e **ajustar conforme o desempenho do LLM**.
    *   Documentar a instrução em um formato fácil de atualizar (ex: arquivo YAML/JSON ou no próprio código) para facilitar a manutenção.

**Atividade 6: Consideração de Frameworks e Ferramentas para Auxílio à Implementação (Opcional)**

1.  **6.1. Avaliar Frameworks de Orquestração de LLMs:**
    *   Considerar o uso de bibliotecas e frameworks como **LangChain**, **Google Agent Development Kit (ADK)**, **AutoGen**, **CrewAI**, **LangGraph** ou **LlamaIndex** para agilizar o desenvolvimento e gerenciar a orquestração multi-agente.
    *   Essas ferramentas podem simplificar o parsing de respostas do LLM, formatos de saída e integração com memória.

2.  **6.2. Utilizar FastAPI para Implementação Customizada:**
    *   Se houver preferência por uma abordagem "faça você mesmo" com mais controle, usar o **FastAPI** para criar endpoints eficientes para cada agente e para o coordenador.

**Atividade 7: Manutenção e Adição de Novos Agentes**

1.  **7.1. Adicionar Novos Agentes Facilmente:**
    *   Garantir que o processo de adicionar novos agentes seja simples: basta **desenvolver a nova função/microserviço** e **registrá-la** para que o coordenador passe a conhecê-la.

2.  **7.2. Atualizar Descrições e a Instrução do Coordenador:**
    *   Ao adicionar novos agentes, **atualizar a instrução do coordenador** (o prompt) para incluir o novo agente na lista de recursos disponíveis e, se necessário, nas regras de decisão.
