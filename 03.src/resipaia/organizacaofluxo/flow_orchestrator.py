# C:\source\IAResipa\03.src\resipaia\organizacaofluxo\flow_orchestrator.py

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END

# Atividade 1: Definição do Estado do Grafo
class ReservationState(TypedDict):
    """Representa o estado da conversa sobre reservas."""
    user_message: str
    phone_number: str
    intent: Literal[
        "check_user", "check_availability", "make_reservation", 
        "cancel_reservation", "check_reservations", "join_waitlist", 
        "general_query", ""
    ]
    sql_query: str | None
    sql_result: dict | None
    response: str | None
    user_id: int | None
    is_registered: bool

# Stubs para os nós do grafo (a serem implementados em outros módulos)
def classify_intent(state: ReservationState) -> ReservationState:
    """Nó para classificar a intenção do usuário (placeholder)."""
    print("Executando nó: classify_intent")
    # Lógica de classificação será implementada em 'responderaoUsuario'
    # Por agora, simulamos uma classificação para roteamento
    if "disponibilidade" in state["user_message"]:
        state["intent"] = "check_availability"
    else:
        state["intent"] = "general_query"
    return state

def check_user(state: ReservationState) -> ReservationState:
    """Nó para verificar se o usuário está cadastrado (placeholder)."""
    print("Executando nó: check_user")
    # Lógica de banco de dados será implementada aqui
    state["is_registered"] = True # Simulação
    state["user_id"] = 123
    if not state["is_registered"]:
        state["response"] = "Usuário não cadastrado. Responda com 'cadastro' para iniciar."
    return state

def execute_logic(state: ReservationState) -> ReservationState:
    """Nó para executar a lógica de negócio baseada na intenção (placeholder)."""
    print(f"Executando nó: execute_logic para a intenção {state['intent']}")
    # Lógica de execução de SQL ou outra lógica de negócio
    state["sql_result"] = {"data": "dados do banco de dados"} # Simulação
    return state

def format_response(state: ReservationState) -> ReservationState:
    """Nó para formatar a resposta final ao usuário (placeholder)."""
    print("Executando nó: format_response")
    # Lógica de formatação será implementada em 'responderaoUsuario'
    if state.get("sql_result"):
        state["response"] = f"Resposta formatada para: {state['sql_result']}"
    elif not state.get("response"):
        state["response"] = "Não entendi, pode repetir?"
    return state

# Atividade 2: Estrutura do Grafo
workflow = StateGraph(ReservationState)

# Adicionar Nós
workflow.add_node("classify_intent", classify_intent)
workflow.add_node("check_user", check_user)
workflow.add_node("execute_logic", execute_logic)
workflow.add_node("format_response", format_response)

# Definir Arestas
workflow.set_entry_point("classify_intent")
workflow.add_edge("classify_intent", "check_user")

# Roteamento condicional após a verificação do usuário
def route_after_user_check(state: ReservationState) -> Literal["execute_logic", "format_response"]:
    """Decide o próximo passo com base no registro do usuário."""
    if state["is_registered"]:
        return "execute_logic"
    else:
        return "format_response"

workflow.add_conditional_edges(
    "check_user",
    route_after_user_check,
    {
        "execute_logic": "execute_logic",
        "format_response": "format_response"
    }
)

workflow.add_edge("execute_logic", "format_response")
workflow.add_edge("format_response", END)

# Compilar o grafo
app = workflow.compile()

# Exemplo de como invocar o grafo (para testes futuros)
if __name__ == "__main__":
    initial_state = {
        "user_message": "qual a disponibilidade de quadras?",
        "phone_number": "+5511987654321",
        "is_registered": False, # O estado inicial não sabe se está registrado
        # O resto dos campos são inicializados como None ou vazios
        "intent": "",
        "sql_query": None,
        "sql_result": None,
        "response": None,
        "user_id": None,
    }
    final_state = app.invoke(initial_state)
    print("--- Estado Final ---")
    print(final_state)
