# Atividade 1: Design e Definição da Arquitetura Multi-Agente

- [ ] **1.1. Definir o Papel do Agente Coordenador:**
    - [ ] Estabelecer um **Agente Coordenador central**, preferencialmente um **LLM (Large Language Model) como o Google Gemini**, que atuará como o "cérebro" do sistema.
    - [ ] O coordenador será responsável por interpretar as instruções do usuário, consultar o contexto armazenado e **decidir qual agente especializado chamar** para cada solicitação.
    - [ ] Compreender que o coordenador seguirá o padrão de **"Coordenador/Dispatcher"**, roteando pedidos para agentes especialistas.

- [ ] **1.2. Identificar e Conceituar Agentes Especializados:**
    - [ ] Dividir a aplicação em **múltiplos agentes especializados**, cada um focado em uma única função específica (por exemplo, "criar pedido", "cancelar pedido", "verificar estoque", "agente de pagamento", "agente de suporte técnico").
    - [ ] Planejar a capacidade de ter **cerca de 20 (ou mais) agentes especializados**, à medida que o sistema cresce.
