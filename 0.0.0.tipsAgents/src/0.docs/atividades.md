# Análise e Plano de Ação para Comandos de Agente

## Análise e Conclusões

1.  **Não há Lógica de Comando Explícita:** O `MCPServer` e o `Router` **não** possuem uma lógica para interpretar "comandos" diretos como `criar agente` ou `remover agente`.
2.  **Roteamento Baseado em IA:** O fluxo principal em `MCPServer.handle_request` é totalmente dependente de uma análise prévia feita por um modelo de linguagem.
3.  **`creator_agent` é Apenas uma Definição Teórica:** A execução da ação não está implementada no roteador.
4.  **Funcionalidade de Remoção Inexistente:** Não há lógica para remover um agente.

## Lacuna Principal

O sistema está configurado para rotear solicitações para serviços de IA, mas não para executar ações locais no sistema de arquivos.

---

## Plano de Ação Proposto

1.  **Criar o Módulo de Remoção:** Criar um novo script `agente_remover/remover.py` com a função `remove_agent(agent_name: str)`.
2.  **Modificar o `MCPServer` para ser um "Orquestrador de Comandos":** Alterar a lógica de `handle_request` para verificar se a solicitação é um comando local (`comando: criar/remover agente`) antes de prosseguir com a análise por IA.

---

## Análise do Erro de Teste (TypeError: NoneType)

### 1. O Erro
`TypeError: argument should be a str or an os.PathLike object where __fspath__ returns a str, not 'NoneType'`

### 2. Causa Raiz
O erro acontece porque `agente_creator.py` e `agente_remover.py` executam `PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT"))` em escopo global. O Pytest importa esses arquivos antes de configurar a variável de ambiente `PROJECT_ROOT` no teste, resultando em `Path(None)` e causando o `TypeError`.

### 3. Solução Aplicada
A correção foi mover a inicialização de `PROJECT_ROOT` do escopo global para dentro das funções que a utilizam (`create_agent` e `remove_agent`). Isso garante que a variável de ambiente seja lida apenas no momento da execução do teste, quando já está configurada.

---

## Análise do Erro de Teste (AssertionError: 404 Not Found)

### 1. O Erro
Ao executar o teste de integração, ocorreu o seguinte erro:
```
FAILED test/test_commands_integration.py::test_create_and_remove_agent_via_server - assert 404 == 200
```

### 2. Causa Raiz
O erro `404 Not Found` indica que a rota `/analyze` não existe no servidor que o `TestClient` está usando. Isso acontece porque o teste, em `test_commands_integration.py`, importa o objeto `app` do FastAPI, mas **nunca cria uma instância da classe `MCPServer`**.

A lógica que registra as rotas no `app` (incluindo `/analyze`) está no método `setup_routes()`, que é chamado apenas pelo construtor `__init__` da classe `MCPServer`. Sem uma instância, as rotas nunca são registradas, e o `TestClient` está testando uma aplicação vazia.

### 3. Solução Proposta
A correção é garantir que uma instância de `MCPServer` seja criada antes que o `TestClient` seja usado. Isso deve ser feito na fixture `test_client` dentro do arquivo `test_commands_integration.py`.

**Arquivo a ser modificado: `test/test_commands_integration.py`**

*Código Antigo (Problemático):*
```python
# ...
from agente_roteador.src.server import app

@pytest.fixture(scope="module")
def test_client():
    """Cria um cliente de teste para a aplicação FastAPI."""
    with TestClient(app) as client:
        yield client
```

*Código Novo (Corrigido):*
```python
# ...
# Importar também a classe MCPServer
from agente_roteador.src.server import app, MCPServer 

@pytest.fixture(scope="module")
def test_client():
    """Cria um cliente de teste para a aplicação FastAPI."""
    # Criar uma instância do servidor para garantir que as rotas sejam registradas
    server_instance = MCPServer() 
    with TestClient(app) as client:
        yield client
```
Esta alteração simples garante que a aplicação de teste esteja totalmente configurada com todas as suas rotas antes de qualquer requisição ser feita, resolvendo o erro 404.
