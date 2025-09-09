# Regras de Roteamento do Agente Roteador

## 1. Princípios Gerais
- Toda solicitação deve ser analisada por completo antes da decisão
- Em caso de dúvida, priorizar o agente mais especializado
- Manter registro da decisão e seu raciocínio para aprendizado futuro

## 2. Critérios de Classificação

### 2.1 Agente Creator (Prioridade 1)
Rotear para este agente quando a solicitação:
- Contiver palavras-chave: "criar agente", "novo agente", "desenvolver agente"
- Solicitar criação de novas capacidades no sistema
- Mencionar necessidade de novo tipo de processamento

### 2.2 Agente Quality (Prioridade 2)
Rotear para este agente quando a solicitação:
- Contiver palavras-chave: "analisar qualidade", "verificar consistência", "avaliar"
- Questionar a qualidade ou eficácia de agentes existentes
- Solicitar análise de conformidade ou padrões

### 2.3 Agente Fluxos (Prioridade 3)
Rotear para este agente quando a solicitação:
- Contiver palavras-chave: "fluxo", "diagrama", "visualizar", "mapa"
- Pedir representação visual de processos
- Solicitar documentação de fluxos de trabalho

### 2.4 Agente Implementador (Prioridade 4)
Rotear para este agente quando a solicitação:
- Contiver palavras-chave: "implementar", "desenvolver", "codificar"
- Solicitar criação ou modificação de código
- Pedir implementação de funcionalidades específicas

## 3. Regras de Divisão de Tarefas
1. Dividir a solicitação quando:
   - Múltiplos domínios de conhecimento são necessários
   - A tarefa tem dependências sequenciais claras
   - Diferentes aspectos precisam ser tratados por agentes distintos

2. Ordem de execução em divisões:
   - Quality -> Creator -> Implementador -> Fluxos
   - Creator -> Quality -> Implementador
   - Implementador -> Quality -> Fluxos

## 4. Critérios de Rejeição
Rejeitar a solicitação quando:
1. Não houver agente capacitado para a tarefa
2. A solicitação for ambígua ou incompleta
3. A solicitação violar políticas do sistema

## 5. Aprendizado e Adaptação
1. Registrar em log:
   - Decisão tomada
   - Raciocínio utilizado
   - Resultado do processamento (sucesso/falha)
   
2. Ajustar regras quando:
   - Um agente rejeitar uma tarefa roteada
   - Uma decisão resultar em erro
   - Padrões novos forem identificados
