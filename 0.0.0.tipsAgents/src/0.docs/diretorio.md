# Análise do Diretório

Este documento descreve a estrutura de diretórios e arquivos do projeto.

## /agente_creator

Este diretório contém os arquivos para um "agente criador".

- **agent.yaml**: Arquivo de configuração para o agente.
- **agente_creator.py**: Script principal para o agente criador.
- **prompt.md**: Arquivo Markdown que provavelmente contém os prompts para o agente.

### /agente_creator/config

- **agent.yaml**: Outro arquivo de configuração do agente.

### /agente_creator/src

- **agent_creator.py**: Código fonte para o agente criador.
- **mcpclient.py**: Um cliente para um serviço chamado "MCP".
- **models.py**: Script Python que define os modelos de dados.
- **templates.py**: Script Python para manipulação de templates.

## /agente_roteador

Este diretório contém uma aplicação mais complexa, um "agente roteador".

- **.env.example**: Exemplo de variáveis de ambiente.
- **.gitignore**: Arquivo para ignorar arquivos no Git.
- **COMPILE.md**: Arquivo Markdown com instruções de compilação.
- **main.py**: Ponto de entrada principal da aplicação.
- **mcp-server.spec**: Arquivo de especificação, provavelmente para o PyInstaller.
- **pyproject.toml**: Arquivo de configuração de projeto e build.
- **setup.py**: Script de setup de pacote Python.

### /agente_roteador/compile

Scripts para compilar a aplicação.

#### /agente_roteador/compile/databricks

Scripts para deploy no Databricks.

- **build_wheel.cmd**: Script para construir o wheel do projeto.
- **deploy.cmd**: Script para deploy.
- **deploy.sh**: Script de deploy para ambiente shell.
- **example_notebook.py**: Exemplo de notebook para Databricks.
- **install.cmd**: Script de instalação.
- **pyproject.toml**: Arquivo de configuração do projeto para o Databricks.
- **README.md**: Instruções para o deploy no Databricks.

#### /agente_roteador/compile/windows

Scripts para deploy no Windows.

- **criarexe.cmd**: Script para criar um executável.
- **install.cmd**: Script de instalação para Windows.

### /agente_roteador/src/agente_roteador

Código fonte principal do agente roteador.

- **__init__.py**: Transforma o diretório em um pacote Python.
- **adapters.py**: Adaptadores para serviços externos.
- **api.py**: Definições de API.
- **cache.py**: Mecanismos de cache.
- **config.py**: Configuração da aplicação.
- **errors.py**: Definições de erros customizados.
- **models.py**: Modelos de dados.
- **monitoring.py**: Lógica de monitoramento.
- **router.py**: Lógica principal de roteamento.
- **security.py**: Código relacionado a segurança.
- **server.py**: Implementação do servidor.

#### /agente_roteador/src/agente_roteador/config

Arquivos de configuração para o agente roteador.

- **capabilities.yaml**: Define as capacidades do agente.
- **prompts.md**: Prompts para o agente.
- **routing_rules.md**: Regras de roteamento em Markdown.
- **routing_rules.yaml**: Regras de roteamento em YAML.
- **sources.yaml**: Definições de fontes de dados.

##### /agente_roteador/src/agente_roteador/config/schemas

- **mcp_request.json**: Schema JSON para requisições MCP.

### /agente_roteador/test

Arquivos de teste.

- **doc.md**: Documentação para os testes.
- **novos.md**: Mais documentação.
- **test_server.py**: Testes para o servidor.

### /agente_roteador/tmp

Arquivos temporários.

- **diretorio.md**: Arquivo temporário de diretório.
- **novidade.md**: Arquivo temporário de novidades.
- **novidadecopilot.md**: Arquivo temporário de novidades do Copilot.
- **novigpt.md**: Arquivo temporário de novidades do GPT.
