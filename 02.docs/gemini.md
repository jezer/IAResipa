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

- **2.1. `02.docs/00.rules/`**: Contém as regras fundamentais e convenções do projeto. Para detalhes, consulte os arquivos específicos:
  - [01. Regras de Gestão de Atividades](00.rules/01.activity_management.md)
  - [02. Convenções de Código (Python)](00.rules/02.coding_conventions.md)
  - [03. Convenções de Documentação](00.rules/03.documentation_conventions.md)
  - [04. Exceções de Pastas](00.rules/04.folder_exceptions.md)
  - [05. Regras de Operações Git](00.rules/05.git_operations.md)
  - [06. Regras de Idioma e Estilo Geral](00.rules/06.language_and_style.md)
  - [08. Regras de Nomenclatura](00.rules/08.naming_conventions.md)

- **2.2. Estrutura de Documentação Adicional:** Além das regras, a pasta `02.docs/` pode conter subpastas temáticas para documentação mais aprofundada, como no exemplo abaixo:
  ```
  02.docs/
  ├── 📄 00.README.md                     # Visão geral do repositório
  ├── 📂 00.rules/                       # Regras e convenções (como listado acima)
  ├── 📂 01.templates/                    # Modelos reutilizáveis
  ├── 📂 02.arquitetura/                   # Padrões e decisões arquiteturais
  ├── 📂 03.objetivo/                     # Documentação de objetivos e soluções principais (ex: sistema de reserva)
  ├── 📂 04.activities/                   # Gerenciamento de atividades e checklists
    ├── [01. Checklist do Projeto: Sistema de Reserva via WhatsApp](04.activities/01.whatsapp_reservation_project.md)
    ├── [02. Checklist de Melhorias nas Regras](04.activities/02.rule_improvements_checklist.md)
    ├── [03. Checklist de Atividades: Configuração do Ambiente](04.activities/03.configuration_activities.md)
    ├── [04. Checklist de Atividades: Criação e Configuração de Workflows n8n](04.activities/04.n8n_workflows_activities.md)
    ├── [05. Checklist de Atividades: Desenvolvimento de Scripts Python](04.activities/05.python_scripts_activities.md)
    ├── [06. Checklist de Atividades: Fase de Testes](04.activities/06.testing_activities.md)
  ├── 📂 05.processos/                     # Metodologias e workflows
  ├── 📂 06.ia_ml/                         # Regras para IA e Machine Learning
  ├── 📂 07.banco_de_dados/                # Normas para bancos de dados
  ├── 📂 08.sistemas/                      # Infraestrutura e cloud
  └── 📂 09.seguranca/                     # Políticas de segurança
  ```
  ```

  03.src/                                # Código fonte principal da aplicação
  ```

  ```
  04.deploy/                             # Arquivos de configuração de deploy (Docker, etc.)
  ```
  ```

  Para pastas que contêm código-fonte ou componentes de sistema (ex: `03.src/`, `04.deploy/`), a nomenclatura pode seguir um padrão de letras e underscores para categorização interna, como `A_db` ou `AA_db`, conforme detalhado nas regras de nomenclatura.

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
2.  **Numeração de Pastas e Arquivos:** Sempre numere todas as novas pastas e arquivos (exceto `gemini.md`) para manter a ordem e a clareza. Para pastas e arquivos existentes, aplique a numeração se ainda não estiverem numerados.
3.  **Seguir a Hierarquia de Pastas:** Respeite e mantenha a estrutura de pastas já estabelecida no projeto para todos os arquivos novos ou modificados.

## 4.3. Outras Instruções
- **Idioma de Resposta:** Sempre responda em português do Brasil.
- **Numeração:** Sempre numere todos os títulos, subtítulos, pastas e arquivos para manter a ordem e a clareza. A única exceção é o arquivo `gemini.md`. **Importante:** Os números devem ser únicos dentro do mesmo nível de diretório (para pastas e arquivos), facilitando a referência como `XX->YY` (ex: `00->01` para `00.rules/01.activity_management.md`).
- **Documentação:** Ao gerar documentação, siga o estilo dos arquivos `.md` existentes.
- **Diagramas:** Ao ser solicitado para criar um fluxo ou diagrama, gere o código em formato Mermaid (`.mmd`).
- **Log:** Sempre guarde todas as execuções no arquivo de log_yyyy_mm_dd_hh_MM_ss.txt
- **Commits:** Ao final de um conjunto de alterações bem-sucedidas, execute o script `powershell.exe -ExecutionPolicy Bypass -File .\01.commands\git_auto_commit.ps1` para registrar o trabalho.
