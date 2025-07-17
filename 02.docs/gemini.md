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

As convenções e regras do projeto estão centralizadas na pasta `02.docs/` para garantir consistência e clareza. Para detalhes sobre regras específicas (gestão de atividades, código, documentação, Git, etc.), consulte os arquivos em `02.docs/00.rules/`.

A estrutura de pastas do projeto é a seguinte:

```
02.docs/                               # Documentação e regras do projeto
├── 📂 00.rules/                       # Regras e convenções fundamentais
├── 📂 01.referencias/                 # Arquivos JSON de mapeamento de dependências
├── 📂 01.templates/                    # Modelos reutilizáveis
├── 📂 02.arquitetura/                   # Padrões e decisões arquiteturais
├── 📂 03.objetivo/                     # Documentação de objetivos e soluções principais
├── 📂 04.activities/                   # Gerenciamento de atividades e checklists
└── ... (outras pastas temáticas)

03.src/                                # Código fonte principal da aplicação
└── resipaia/                          # Raiz da biblioteca Python (sem prefixos)

04.deploy/                             # Arquivos de configuração de deploy (Docker, etc.)
```

**Regras de Nomenclatura:**
- Pastas e arquivos (exceto `gemini.md`) devem ser numerados para manter a ordem e clareza (ex: `00.rules/01.activity_management.md`).
- Números devem ser únicos dentro do mesmo nível de diretório.
- Para pastas que contêm código-fonte ou componentes de sistema (ex: `03.src/`, `04.deploy/`), a nomenclatura pode seguir um padrão de letras e underscores para categorização interna (ex: `A_db`).
- **Exceção:** A pasta raiz de uma biblioteca Python (ex: `resipaia` dentro de `03.src/`) deve conter apenas o nome da biblioteca, sem prefixos ou numeração.

# 3. Instruções para o Gemini

## 3.1. Diretrizes Operacionais

- **Prioridade:** Sua principal prioridade é a estabilidade e a consistência do projeto.
- **Análise Prévia:** Antes de executar qualquer instrução ou realizar alterações, analise sempre as regras existentes e o contexto do projeto.
- **Conflitos:** Se uma ação solicitada contradizer uma regra pré-existente ou puder criar um loop de execução infinito, **interrompa a execução** e informe o conflito ou o potencial loop.
- **Processo de Alteração:**
    1.  **Regras:** Ao criar ou modificar regras, separe-as em:
        *   **Genéricas:** Reutilizáveis para futuros projetos.
        *   **Personalizadas:** Específicas para a arquitetura deste projeto.
    2.  **Estrutura:** Respeite e mantenha a hierarquia de pastas estabelecida.
    3.  **Numeração:** Sempre numere novas pastas e arquivos (exceto `gemini.md`). Para arquivos existentes, aplique a numeração se ainda não estiverem numerados.
    4.  **Atualização de Referências:** Após qualquer alteração na estrutura de pastas, criação ou movimentação de arquivos de código ou documentação, é **CRÍTICO** atualizar os arquivos JSON de referência correspondentes na pasta `02.docs/01.referencias/`. Isso garante que o mapeamento de dependências do projeto esteja sempre preciso e atualizado.

## 3.2. Mapeamento de Dependências e Regras

**CRÍTICO:** Antes de realizar *qualquer* alteração, **SEMPRE** consulte o arquivo JSON de mapeamento de dependências correspondente na pasta `02.docs/01.referencias/`. Por exemplo, para a pasta `05.wahaconnect`, consulte `00.05.wahaconnect.json`; para `00.rules`, consulte `00.00.rules.json`.

As regras de codificação e teste de Python foram consolidadas na pasta `02.docs/00.rules/02.coding/`. Consulte os arquivos nesta pasta para obter as diretrizes mais recentes.

Estes arquivos JSON detalham as relações e dependências entre os documentos de design, atividades e arquivos de código-fonte, garantindo que as alterações sejam feitas de forma consistente, sem contradições e alinhadas com os objetivos do projeto.

## 3.3. Outras Instruções

- **Idioma:** Sempre responda em português do Brasil.
- **Documentação:** Ao gerar documentação, siga o estilo dos arquivos `.md` existentes.
- **Diagramas:** Ao ser solicitado para criar um fluxo ou diagrama, gere o código em formato Mermaid (`.mmd`).
- **Log:** Sempre registre todas as execuções em um arquivo de log (ex: `log_yyyy_mm_dd_hh_MM_ss.txt`).
- **Commits:** Ao final de um conjunto de alterações bem-sucedidas, execute o script `powershell.exe -ExecutionPolicy Bypass -File .\01.commands\git_auto_commit.ps1` para registrar o trabalho.
