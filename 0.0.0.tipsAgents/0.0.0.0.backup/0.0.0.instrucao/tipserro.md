# Análise Preliminar da Estrutura de Pastas

[1] Após uma revisão inicial da estrutura de pastas e da documentação, foram identificadas algumas inconsistências e oportunidades de melhoria, resultando em uma nova proposta de arquitetura focada em agentes auto-contidos e independentes.

## Pontos de Inconsistência (Arquitetura Anterior)

[2] 1.  **Centralização de Regras**: A arquitetura anterior propunha a centralização de regras em arquivos globais, o que entrava em conflito com o objetivo de ter agentes independentes e auto-contidos.

[3] 2.  **Estrutura de Pastas Confusa**: A presença de agentes nas pastas `0.0.Global/` e `1.0.agentes_especificos/` criava uma estrutura confusa e dificultava a identificação das responsabilidades de cada agente.

## Nova Proposta de Arquitetura: Agentes Independentes

[4] A nova arquitetura se baseia no princípio de que cada agente é uma unidade de software independente, com suas próprias regras, documentação e código-fonte. O `agente_roteador` atuará como uma biblioteca de roteamento, sendo o ponto de entrada para a comunicação entre os agentes.

### Estrutura de um Agente

[5] Cada agente terá a seguinte estrutura de pastas:

```
/src/
  ├── {nome_do_agente}/
  │   ├── src/                # Código fonte do agente
  │   │   └── ...
  │   ├── docs/               # Documentação específica do agente
  │   │   ├── prompt.md
  │   │   └── agent.yaml
  │   ├── rules/              # Regras específicas do agente
  │   │   └── ...
  │   ├── input/              # Pasta de entrada para comunicação
  │   └── output/             # Pasta de saída para comunicação
```

### O Papel do `agente_roteador`

[6] O `agente_roteador` será tratado como uma biblioteca independente, responsável por rotear as solicitações para os agentes corretos com base em um conjunto de regras de roteamento. Ele não terá conhecimento da lógica de negócio dos outros agentes.

### Vantagens da Nova Arquitetura

[7] *   **Autonomia dos Agentes**: Cada agente é responsável por suas próprias regras e documentação, o que facilita a manutenção e o desenvolvimento.
*   **Clareza e Simplicidade**: A estrutura de pastas é mais clara e consistente, facilitando a navegação e o entendimento do projeto.
*   **Reutilização**: O `agente_roteador` pode ser reutilizado em outros projetos como uma biblioteca de roteamento.

## Plano de Implementação

[8] Para implementar a nova arquitetura, os seguintes passos são necessários:

[9] 1.  [ ] **Reestruturar as Pastas**: Mover todos os agentes para a pasta `src/` e aplicar a nova estrutura de pastas para cada agente.

[10] 2.  [ ] **Mover as Regras**: Mover as regras globais para as pastas `rules/` de cada agente correspondente.

[11] 3.  [x] **Refatorar o `agente_roteador`**: Transformar o `agente_roteador` em uma biblioteca independente.

[12] 4.  [ ] **Atualizar a Documentação**: Atualizar a documentação do projeto para refletir a nova arquitetura.

## Implementação: Refatorando o `agente_roteador`

[13] O foco inicial será na refatoração do `agente_roteador`. As seguintes atividades serão executadas:

[14] 1.  **Criação da Nova Estrutura de Pastas**:
    *   [x] Criar a pasta `src/agente_roteador/`.
    *   [x] Dentro de `src/agente_roteador/`, criar as subpastas: `src/`, `docs/`, `rules/`, `input/`, e `output/`.

[15] 2.  **Movimentação dos Arquivos Existentes**:
    *   [x] Mover `src/agente_roteador/agente_roteador.py` para `src/agente_roteador/src/agente_roteador.py`.
    *   [x] Mover `src/agente_roteador/agent.yaml` para `src/agente_roteador/docs/agent.yaml`.
    *   [x] Mover `src/agente_roteador/prompt.md` para `src/agente_roteador/docs/prompt.md`.

[16] 3.  **Criação do Arquivo de Regras**:
    *   [x] Criar um novo arquivo `rules.md` em `src/agente_roteador/rules/`.
    *   [x] O arquivo `rules.md` conterá as regras de roteamento que o `agente_roteador` utilizará para direcionar as solicitações.

[17] 4.  **Atualização do `agent.yaml`**:
    *   [x] O arquivo `src/agente_roteador/docs/agent.yaml` será atualizado para refletir a nova estrutura de pastas e a localização do arquivo de regras.