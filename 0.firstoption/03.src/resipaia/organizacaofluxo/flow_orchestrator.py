# C:\source\IAResipa\03.src\resipaia\organizacaofluxo\flow_orchestrator.py

from typing import Literal
from langgraph.graph import StateGraph, END
from resipaia.A_db.db_00_supabase_config import get_supabase_client
from resipaia.responderaoUsuario.response_generator import classify_intent_with_llm, format_response_with_llm
from resipaia.common.types import ReservationState

# Initialize Supabase client globally or pass it around
supabase_client = get_supabase_client()

def check_user(state: ReservationState) -> ReservationState:
    """Nó para verificar se o usuário está cadastrado no Supabase."""
    print("Executando nó: check_user")
    phone_number = state["phone_number"]
    try:
        response = supabase_client.from_("cadastro_pessoas_fisica").select("id").eq("phone_number", phone_number).execute()
        if response.data:
            state["is_registered"] = True
            state["user_id"] = response.data[0]["id"]
        else:
            state["is_registered"] = False
            state["response"] = "Usuário não cadastrado. Responda com 'cadastro' para iniciar."
    except Exception as e:
        print(f"Erro ao verificar usuário no Supabase: {e}")
        state["is_registered"] = False # Assume not registered on error
        state["response"] = "Ocorreu um erro ao verificar seu cadastro. Tente novamente."
    return state

def execute_logic(state: ReservationState) -> ReservationState:
    """Nó para executar a lógica de negócio baseada na intenção, interagindo com o Supabase."""
    print(f"Executando nó: execute_logic para a intenção {state['intent']}")
    sql_query = state.get("sql_query")

    if not sql_query:
        state["sql_result"] = {"error": "No SQL query provided for execution."}
        return state

    try:
        # This is a highly simplified and potentially insecure way to execute SQL.
        # It assumes the LLM generates very specific and simple SELECT queries.
        # A robust solution would involve a proper SQL parser or a different LLM output format.

        # Attempt to parse table name from a simple SELECT query
        if sql_query.lower().startswith("select"):
            from_index = sql_query.lower().find("from")
            if from_index != -1:
                table_part = sql_query[from_index + 4:].strip()
                table_name = table_part.split(" ")[0].strip().replace(";", "") # Remove semicolon if present

                # Attempt to parse WHERE clause (very basic)
                where_index = sql_query.lower().find("where")
                if where_index != -1:
                    where_clause = sql_query[where_index + 5:].strip().replace(";", "")
                    # This is where it gets tricky. We need to parse column and value.
                    # For now, let's assume a single 'eq' condition.
                    # Example: "column = 'value'"
                    if "=" in where_clause:
                        col, val = where_clause.split("=", 1)
                        col = col.strip()
                        val = val.strip().strip("'") # Remove quotes

                        response = supabase_client.from_(table_name).select("*").eq(col, val).execute()
                        state["sql_result"] = {"data": response.data}
                    else:
                        state["sql_result"] = {"error": "Complex WHERE clause not supported by simple parser."}
                else:
                    # No WHERE clause, select all
                    response = supabase_client.from_(table_name).select("*").execute()
                    state["sql_result"] = {"data": response.data}
            else:
                state["sql_result"] = {"error": "Could not parse table name from SQL query."}
        else:
            state["sql_result"] = {"error": f"SQL operation for '{state['intent']}' (non-SELECT) not yet implemented or supported."}

    except Exception as e:
        print(f"Erro ao executar lógica no Supabase: {e}")
        state["sql_result"] = {"error": f"Erro ao executar lógica no Supabase: {e}"}
    return state

# Atividade 2: Estrutura do Grafo
workflow = StateGraph(ReservationState)

# Adicionar Nós
workflow.add_node("classify_intent", classify_intent_with_llm) # Use actual LLM function
workflow.add_node("check_user", check_user)
workflow.add_node("execute_logic", execute_logic)
workflow.add_node("format_response", format_response_with_llm) # Use actual LLM function

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
