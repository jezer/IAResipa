
---
title: Mapa Mental da Arquitetura de Agentes
markmap:
  colorFreezeLevel: 2
---

# Arquitetura do Sistema

## `src/` (Código-Fonte e Comunicação)
- **Propósito**: Contém o código, a configuração e as pastas de comunicação de cada agente.
- **Agentes**
  - `agente_roteador`
    - `agente_roteador.py`
    - `agent.yaml`
    - `prompt.md`
    - `input/`
    - `output/`
  - `agente_creator`
    - `...`
    - `input/`
    - `output/`
  - `agente_quality`
    - `...`
    - `input/`
    - `output/`
  - ... outros

## `0.0.Global/2.0.docs/` (Documentação)
- **Propósito**: Documentação conceitual do sistema.
- **Documentos Chave**
  - `0.0.plano_de_projeto.md`
  - `0.1.regras_globais.md`
  - `0.2.arquitetura_pastas.md`
  - `0.4.protocolo_comunicacao.md`
