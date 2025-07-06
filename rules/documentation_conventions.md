# Convenções de Documentação

*   **Localização:** Toda a documentação relacionada a um arquivo de código específico deve residir na pasta `docs`.
*   **Estrutura de Pastas em `docs`:
    *   Para **qualquer arquivo** que necessite de documentação detalhada (seja um arquivo Python em `src/`, um script em `commands/`, etc.), crie uma estrutura de pastas dentro de `docs/` que espelhe o caminho relativo do arquivo original.
    *   A documentação para um arquivo específico deve ser um arquivo Markdown (`.md`) com o **mesmo nome base** do arquivo original.
    *   **Exemplos:
        *   Para `src/1.Ingestao/A.ingestao_de_arquivos/main_ingestao.py`, a documentação estará em `docs/src/1.Ingestao/A.ingestao_de_arquivos/main_ingestao.md`.
        *   Para `commands/git_auto_commit.ps1`, a documentação estará em `docs/commands/git_auto_commit.md`.
    *   **Evitar Repetição de Nomes:** Garanta que os nomes dos arquivos de código sejam únicos em todo o projeto para que a estrutura de documentação funcione sem ambiguidades.
*   **Nomenclatura de Arquivos de Documentação:**
    *   O arquivo de documentação principal para uma unidade de código (ex: `docs/commands/git_auto_commit.md`) deve ter o **mesmo nome base** do arquivo de código que ele documenta.
    *   Para arquivos de documentação **suplementares** dentro de uma pasta de documentação (ex: `docs/src/meu_modulo/`), use nomes descritivos, em minúsculas e separados por hífens (ex: `visao_geral.md`, `uso.md`, `referencia_api.md`, `fluxo_dados.mmd`).
*   **Formato:**
    *   **Texto:** Markdown (`.md`).
    *   **Diagramas:** Mermaid (`.mmd`). Para diagramas de classe, siga a sintaxe oficial em [Mermaid Class Diagram](https://mermaid.js.org/syntax/classDiagram.html). Um exemplo básico pode ser encontrado em [mermaid_class_diagram_example.md](mermaid_class_diagram_example.md).
*   **Idioma:** Português do Brasil (pt-BR), conforme já estabelecido.
*   **Conteúdo Mínimo por Módulo/Arquivo de Código:**
    *   `visao_geral.md`: Uma descrição de alto nível do propósito do módulo/arquivo.
    *   `uso.md`: Exemplos de como usar as funções ou classes principais.
    *   `referencia_api.md` (opcional, se a docstring não for suficiente): Detalhes sobre funções, classes, parâmetros e valores de retorno.
    *   `fluxo_dados.mmd` (opcional): Diagramas de fluxo ou sequência usando Mermaid para explicar a lógica interna.