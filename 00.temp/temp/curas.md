
## 5. Validação do Usuário no Supabase

É importante notar que o `test_response_generator.py` **não** é responsável por validar o celular do usuário no banco de dados. Sua única função é interagir com o LLM. A validação do usuário é uma responsabilidade separada, localizada no orquestrador do fluxo.

### Onde a Validação Acontece?

-   **Arquivo:** `C:\source\IAResipa\03.src\resipaia\organizacaofluxo\flow_orchestrator.py`
-   **Função (Nó do Grafo):** `check_user(state: ReservationState)`

### Como Funciona (Implementação Futura)

Dentro do `flow_orchestrator.py`, a função `check_user` foi definida como um *placeholder* (um stub). A lógica real, que ainda será implementada, fará o seguinte:

1.  **Receber o Estado:** A função receberá o estado atual da conversa, que contém o `phone_number` do usuário.
2.  **Conectar ao Supabase:** Ela usará um cliente Supabase (que será configurado no projeto) para se conectar ao banco de dados.
3.  **Executar a Consulta:** A função executará uma consulta na tabela `cadastro_pessoas_fisica` para verificar se o `phone_number` existe.
4.  **Atualizar o Estado:** Com base no resultado da consulta, a função atualizará o estado da conversa:
    -   Se o usuário for encontrado, `state['is_registered']` será definido como `True` e `state['user_id']` será preenchido.
    -   Se o usuário não for encontrado, `state['is_registered']` será `False` e uma mensagem de resposta, como `"Usuário não cadastrado..."`, será definida em `state['response']`.

### Separação de Responsabilidades

Essa separação é um princípio de design de software fundamental. O `response_generator` cuida apenas de "conversar" com a IA. O `flow_orchestrator` cuida da lógica de negócio e do fluxo, como "verificar o cadastro de um usuário".

O teste para a função `check_user` está no arquivo `test_flow_orchestrator.py`, que, de forma similar, usa mocks para simular o comportamento do banco de dados, permitindo testar a lógica de roteamento do grafo sem depender de uma conexão real com o Supabase.
