# 1. Contexto do Projeto: IATextHelp/n8n_python_workflow

## 1.1. Sobre o Projeto

Este repositório contém a documentação, protótipos e instruções para um sistema de automação que integra n8n, Python e bancos de dados (PostgreSQL/Supabase). O objetivo principal é explorar o uso de LLMs (como o Gemini) para auxiliar no desenvolvimento, documentação e teste de software.

O projeto está organizado em torno de "instruções" para diferentes modelos de IA, diagramas de fluxo e arquitetura, e protótipos de interfaces.

## 1.2. Tecnologias Principais

- **Linguagem Principal:** Python
- **Automação de Workflow:** n8n
- **Banco de Dados:** PostgreSQL (via Supabase)
- **Diagramas:** Mermaid (`.mmd`) para fluxogramas, diagramas de sequência, mind maps, etc.
- **Idioma:** A grande maioria dos documentos e nomes de arquivos está em português do Brasil (pt-BR).

# 2. Convenções e Estrutura de Documentação

As convenções e regras do projeto estão centralizadas na pasta `02.docs/` para garantir consistência e clareza. A estrutura é organizada da seguinte forma:

- **2.1. `02.docs/03.rules/`**: Contém as regras fundamentais e convenções do projeto. Para detalhes, consulte os arquivos específicos:
  - [01. Regras de Gestão de Atividades](03.rules/01.activity_management.md)
  - [02. Convenções de Código (Python)](03.rules/02.coding_conventions.md)
  - [03. Convenções de Documentação](03.rules/03.documentation_conventions.md)
  - [04. Exceções de Pastas](03.rules/04.folder_exceptions.md)
  - [05. Regras de Operações Git](03.rules/05.git_operations.md)
  - [06. Regras de Idioma e Estilo Geral](03.rules/06.language_and_style.md)

- **2.2. Estrutura de Documentação Adicional:** Além das regras, a pasta `02.docs/` pode conter subpastas temáticas para documentação mais aprofundada, como no exemplo abaixo:
  ```
  02.docs/
  ├── 📄 00.README.md                     # Visão geral do repositório
  ├── 📂 01.rules/                       # Regras e convenções (como listado acima)
  ├── 📂 02.arquitetura/                   # Padrões e decisões arquiteturais
  ├── 📂 03.processos/                     # Metodologias e workflows
  ├── 📂 04.ia_ml/                         # Regras para IA e Machine Learning
  ├── 📂 05.banco_de_dados/                # Normas para bancos de dados
  ├── 📂 06.sistemas/                      # Infraestrutura e cloud
  ├── 📂 07.seguranca/                     # Políticas de segurança
  └── 📂 08.templates/                     # Modelos reutilizáveis
  ```

# 3. Instruções para IAs

Note que existem arquivos específicos para diferentes modelos (`gemini_...`, `dpseek_...`, `gpt_...`). Ao gerar novas instruções, siga este padrão.

# 4. Instruções Específicas para o Gemini

## 4.1. Diretriz Crítica de Segurança
**ESSENCIAL:** Antes de executar qualquer instrução, analise as regras existentes.
- **Conflito de Regras:** Se uma nova regra ou ação solicitada contradisser uma regra pré-existente, **interrompa a execução** e informe o conflito.
- **Loop Infinito:** Se uma regra ou ação puder criar um loop de execução infinito, **interrompa a execução** e informe o potencial loop.
A sua principal prioridade é a estabilidade e a consistência do projeto.

## 4.2. Processo de Alteração
Ao realizar qualquer alteração no projeto, siga estritamente os seguintes passos:
1.  **Analisar e Estruturar Regras:** Antes de implementar, analise as regras existentes. Ao criar ou modificar regras, separe-as em:
    *   **Regras Genéricas:** Templates reutilizáveis para futuros projetos.
    *   **Regras Personalizadas:** Específicas para a arquitetura deste projeto.
2.  **Seguir a Hierarquia de Pastas:** Respeite e mantenha a estrutura de pastas já estabelecida no projeto para todos os arquivos novos ou modificados.

## 4.3. Outras Instruções
- **Numeração:** Sempre numere todos os títulos, subtítulos, pastas e arquivos para manter a ordem e a clareza. A única exceção é o arquivo `gemini.md`.
- **Documentação:** Ao gerar documentação, siga o estilo dos arquivos `.md` existentes.
- **Diagramas:** Ao ser solicitado para criar um fluxo ou diagrama, gere o código em formato Mermaid (`.mmd`).
- **Log:** Sempre guarde todas as execuções no arquivo de log_yyyy_mm_dd_hh_MM_ss.txt
- **Commits:** Ao final de um conjunto de alterações bem-sucedidas, execute o script `powershell.exe -ExecutionPolicy Bypass -File .\01.commands\git_auto_commit.ps1` para registrar o trabalho.
