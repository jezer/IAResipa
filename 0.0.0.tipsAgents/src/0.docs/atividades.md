# Análise e Plano de Ação para Comandos de Agente

## Análise e Conclusões

1.  **Não há Lógica de Comando Explícita:** O `MCPServer` e o `Router` **não** possuem uma lógica para interpretar "comandos" diretos como `criar agente` ou `remover agente`. O sistema atual é projetado para analisar o *conteúdo semântico* de uma solicitação e roteá-la para o melhor "cliente" (agente de IA) com base em intenção e domínio.
    
    *Trecho Relevante (`agente_roteador/src/server.py`):*
    ```python
    # O fluxo principal é analisar e depois rotear, sem etapa de verificação de "comando"
    analysis = await self._analyze_with_llm(...)
    routing_decision = self.router.apply_rules(analysis=analysis, ...)
    ```

2.  **Roteamento Baseado em IA:** O fluxo principal em `MCPServer.handle_request` é totalmente dependente de uma análise prévia feita por um modelo de linguagem (`_analyze_with_llm`) para extrair uma intenção (`Analysis`) que será usada pelo roteador.

3.  **`creator_agent` é Apenas uma Definição Teórica:** No arquivo `capabilities.yaml`, existe a definição de um `creator_agent` que corresponde à intenção `create_agent`. No entanto, o roteador não tem um mecanismo para *executar* um script Python local como o `agente_creator.py`. Ele apenas "seleciona" o cliente como um destino teórico. A execução da ação não está implementada.

    *Trecho Relevante (`agente_roteador/src/config/capabilities.yaml`):*
    ```yaml
    clients:
      creator_agent:
        id: "creator_agent"
        match:
          intent: ["create_agent", "modify_agent"]
          domains: ["agents", "prompts"]
    ```

4.  **Funcionalidade de Remoção Inexistente:** Como previsto, não há absolutamente nenhuma menção ou lógica para remover um agente em nenhum dos arquivos do projeto.

## Lacuna Principal

O sistema está configurado para rotear solicitações para *serviços de IA externos* ou *clientes definidos*, mas não para executar ***ações locais no sistema de arquivos***, como executar o script `agente_creator.py` ou um futuro script de remoção.

---

## Plano de Ação Proposto

Para implementar a funcionalidade de criação e remoção como comandos diretos, proponho as seguintes modificações:

1.  **Criar o Módulo de Remoção:**
    *   Será criado um novo diretório `agente_remover/` com um script `remover.py`.
    *   Este script conterá a função `remove_agent(agent_name: str)`, responsável por localizar e apagar com segurança o diretório do agente.
    
    *Exemplo da Estrutura do Script:*
    ```python
    # agente_remover/remover.py
    import shutil
    from pathlib import Path

    def remove_agent(agent_name: str, project_root: Path):
        """Localiza e remove o diretório de um agente."""
        agent_dir = project_root / "src" / agent_name
        if agent_dir.exists() and agent_dir.is_dir():
            shutil.rmtree(agent_dir)
            return {"status": "sucesso", "message": f"Agente {agent_name} removido."}
        else:
            return {"status": "erro", "message": "Agente não encontrado."}
    ```

2.  **Modificar o `MCPServer` para ser um "Orquestrador de Comandos":**
    *   A lógica principal do `MCPServer` em `handle_request` será alterada. Antes de qualquer análise por IA, ele verificará se a solicitação é um comando local.
    *   **Nova Lógica Proposta para `handle_request`:**
        1.  Receber a solicitação.
        2.  Verificar se `request.content` começa com um prefixo de comando, como `comando:`.
        3.  **Se for um comando de criação** (ex: `comando: criar agente ...`):
            *   Extrair os dados do agente da string da solicitação.
            *   Importar e chamar diretamente a função `agente_creator.create_agent()`.
            *   Retornar uma resposta imediata sobre o sucesso ou falha da operação.
        4.  **Se for um comando de remoção** (ex: `comando: remover agente <nome_do_agente>`):
            *   Extrair o nome do agente.
            *   Importar e chamar a nova função `agente_remover.remove_agent()`.
            *   Retornar uma resposta imediata.
        5.  **Se não for um comando:**
            *   Manter o fluxo original: executar a análise semântica com IA e o roteamento através do `Router`.

    *Exemplo da Lógica de Desvio no Código:*
    ```python
    # Em agente_roteador/src/server.py -> handle_request

    from agente_creator import agente_creator
    # from agente_remover import remover (após criado)

    async def handle_request(self, request: MCPRequest) -> MCPResponse:
        content = request.content.strip()

        if content.startswith("comando: criar agente"):
            # ... lógica para parsear dados e chamar agente_creator.create_agent(...)
            return MCPResponse(success=True, content="Comando de criação executado.")

        elif content.startswith("comando: remover agente"):
            # ... lógica para parsear nome e chamar remover.remove_agent(...)
            return MCPResponse(success=True, content="Comando de remoção executado.")

        else:
            # Lógica original de análise por IA e roteamento
            analysis = await self._analyze_with_llm(...)
            routing_decision = self.router.apply_rules(...)
            # ... resto do fluxo
    ```
