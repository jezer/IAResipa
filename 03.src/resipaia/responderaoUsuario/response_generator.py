# C:\source\IAResipa\03.src\resipaia\responderaoUsuario\response_generator.py

import os
import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from resipaia.organizacaofluxo.flow_orchestrator import ReservationState

# Atividade 1: Configuração do Cliente e Modelo Gemini
# Assumindo que a API Key está nas variáveis de ambiente
llm = ChatGoogleGenerativeAI(model="gemini-pro")

# Prompt para classificação de intenção, conforme a documentação
intent_prompt_template = ChatPromptTemplate.from_template(
    """Você é um assistente de sistema de reservas. Com base na mensagem do usuário, classifique a intenção e gere uma resposta ou consulta SQL conforme necessário.

Mensagem do Usuário: {user_message}
Número de Telefone do Usuário: {phone_number}

Intenções possíveis:
1. check_user: Verificar se o usuário está registrado.
2. check_availability: Verificar disponibilidade de quiosques ou quadras de beach tennis.
3. make_reservation: Criar uma reserva para um quiosque ou quadra.
4. cancel_reservation: Cancelar uma reserva existente.
5. check_reservations: Visualizar as reservas ativas do usuário.
6. join_waitlist: Entrar na lista de espera para um recurso.
7. general_query: Lidar com perguntas gerais ou intenções desconhecidas.

Instruções:
- Para check_user, gere uma consulta SQL para verificar se o phone_number existe em cadastro_pessoas_fisica.
- Para check_availability, gere uma consulta SQL para encontrar quiosques ou quadras disponíveis para uma data/hora específica.
- Para make_reservation, gere uma consulta SQL para criar uma reserva provisória.
- Para cancel_reservation, gere uma consulta SQL para cancelar uma reserva e verificar a lista de espera.
- Para check_reservations, gere uma consulta SQL para listar as reservas ativas do usuário.
- Para join_waitlist, gere uma consulta SQL para adicionar o usuário à lista de espera.
- Para general_query, forneça uma resposta em linguagem natural ou peça esclarecimentos.

Retorne um objeto JSON com:
- intent: A intenção classificada
- sql_query: A consulta SQL (se aplicável)
- response: A resposta para o usuário (se nenhuma consulta SQL for necessária)

Exemplo:
{{
  "intent": "check_user",
  "sql_query": "SELECT * FROM cadastro_pessoas_fisica WHERE phone_number = '123456789'",
  "response": null
}}
"""
)

# Prompt para formatação de resposta, conforme a documentação
response_formatting_template = ChatPromptTemplate.from_template(
    """Formate o resultado a seguir em uma resposta amigável para o usuário.

Intenção: {intent}
Resultado: {sql_result}

Forneça uma resposta clara e concisa em português.
"""
)

def classify_intent_with_llm(state: ReservationState) -> ReservationState:
    """Usa o LLM para classificar a intenção e extrair informações."""
    prompt = intent_prompt_template.format(
        user_message=state["user_message"],
        phone_number=state["phone_number"]
    )
    
    try:
        result = llm.invoke(prompt)
        parsed_result = json.loads(result.content)
        
        state["intent"] = parsed_result.get("intent", "general_query")
        state["sql_query"] = parsed_result.get("sql_query")
        state["response"] = parsed_result.get("response")
        
    except (json.JSONDecodeError, Exception) as e:
        print(f"Erro ao classificar intenção: {e}")
        state["intent"] = "general_query"
        state["response"] = "Desculpe, não entendi sua solicitação. Pode esclarecer?"
        
    return state

def format_response_with_llm(state: ReservationState) -> ReservationState:
    """Usa o LLM para formatar uma resposta a partir de dados."""
    # Se já temos uma resposta, não faz nada
    if state.get("response"):
        return state

    # Se não há resultado para formatar, retorna resposta padrão
    if not state.get("sql_result"):
        state["response"] = "Não encontrei informações para sua solicitação."
        return state

    prompt = response_formatting_template.format(
        intent=state["intent"],
        sql_result=json.dumps(state["sql_result"])
    )

    try:
        result = llm.invoke(prompt)
        state["response"] = result.content
    except Exception as e:
        print(f"Erro ao formatar resposta: {e}")
        state["response"] = "Ocorreu um erro ao processar sua solicitação. Tente novamente."

    return state
