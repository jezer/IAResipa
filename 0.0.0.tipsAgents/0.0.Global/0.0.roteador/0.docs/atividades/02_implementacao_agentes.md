# Atividade 2: Implementação dos Agentes Especializados

- [ ] **2.1. Codificar Cada Agente como Funções/Microserviços Independentes:**
    - [ ] Implementar cada agente como uma **função ou microserviço Python independente**.
    - [ ] Expor esses agentes via API, utilizando ferramentas como **endpoints REST em FastAPI** ou **funções serverless no Azure Functions**.
    - [ ] Garantir que a **interface de cada agente seja bem definida** com inputs e outputs conhecidos para uma coordenação confiável.

- [ ] **2.2. Habilitar 'Function Calling' para o Gemini:**
    - [ ] Aproveitar o recurso de `function calling` do Gemini, definindo cada agente especializado como uma "**função**" disponível para o modelo coordenador.
    - [ ] Fornecer ao Gemini as **assinaturas e descrições dessas funções** (por exemplo, `criar_pedido(pedido_dados)`, `cancelar_pedido(pedido_id)`) para que ele possa escolher autonomamente a função correta.

- [ ] **2.3. Criar Descrições Claras para Cada Agente:**
    - [ ] Elaborar **descrições claras e padronizadas** para cada agente, explicando sua função (ex: "Agente de Cobrança: lida com questões de pagamento"; "Agente de Suporte: resolve problemas técnicos").
    - [ ] Essas descrições são **fundamentais para ajudar o coordenador** (LLM ou lógica customizada) a decidir corretamente qual agente chamar.
