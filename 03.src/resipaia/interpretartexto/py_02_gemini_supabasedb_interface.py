import sys
import json
import logging
from supabase import Client

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def query_gemini(message_details: dict) -> dict:
    # Placeholder para a lógica real de integração com a API Gemini
    prompt = message_details.get('body')
    logging.info(f"Consultando Gemini com prompt: {prompt}")
    # Simula uma resposta do Gemini
    if "olá" in prompt.lower():
        return {"status": "success", "response": "Olá! Como posso ajudar com suas reservas hoje?"}
    elif "disponibilidade" in prompt.lower():
        return {"status": "success", "response": "Para verificar a disponibilidade, preciso saber o tipo de recurso (quiosque ou quadra) e a data desejada."}
    else:
        return {"status": "success", "response": f"Entendi sua pergunta: '{prompt}'. No momento, estou focado em reservas e pagamentos. Posso ajudar com isso?"}

from ..A_db.db_00_supabase_config import get_supabase_client

def supabase_crud(supabase_client: Client, action: str, table: str, data: dict = None, query: dict = None) -> dict:
    logging.info(f"Ação Supabase: {action} na tabela {table}. Dados: {data}, Query: {query}")
    
    try:

        if action == "insert":
            response = supabase_client.table(table).insert(data).execute()
            return {"status": "success", "data": response.data}
        elif action == "select":
            if query:
                # Assume que a query é um dicionário de filtros
                # Ex: {"id": "some_id"} ou {"name": "some_name"}
                # Para queries mais complexas, a função precisaria ser expandida
                query_builder = supabase_client.table(table).select("*")
                for key, value in query.items():
                    query_builder = query_builder.eq(key, value)
                response = query_builder.execute()
            else:
                response = supabase_client.table(table).select("*").execute()
            return {"status": "success", "data": response.data}
        elif action == "update":
            if not query:
                return {"status": "error", "message": "Query é necessária para a operação de update."}
            query_builder = supabase_client.table(table).update(data)
            for key, value in query.items():
                query_builder = query_builder.eq(key, value)
            response = query_builder.execute()
            return {"status": "success", "data": response.data}
        elif action == "delete":
            if not query:
                return {"status": "error", "message": "Query é necessária para a operação de delete."}
            query_builder = supabase_client.table(table).delete()
            for key, value in query.items():
                query_builder = query_builder.eq(key, value)
            response = query_builder.execute()
            return {"status": "success", "data": response.data}
        else:
            return {"status": "error", "message": "Ação Supabase inválida."}
    except Exception as e:
        logging.error(f"Erro na operação Supabase {action}: {e}")
        return {"status": "error", "message": str(e)}

def main():
    action = sys.argv[1] if len(sys.argv) > 1 else None
    
    response = {"status": "error", "message": "Ação inválida."}

    if action == "--query-gemini" and len(sys.argv) > 2:
        try:
            message_details = json.loads(sys.argv[2])
            response = query_gemini(message_details)
        except json.JSONDecodeError:
            response = {"status": "error", "message": "Detalhes da mensagem inválidos (JSON)."}
    elif action == "--supabase-crud" and len(sys.argv) > 3:
        crud_action = sys.argv[2]
        table_name = sys.argv[3]
        data = json.loads(sys.argv[4]) if len(sys.argv) > 4 else None
        query = json.loads(sys.argv[5]) if len(sys.argv) > 5 else None
        supabase = get_supabase_client()
        response = supabase_crud(supabase, crud_action, table_name, data, query)
    
    print(json.dumps(response))

if __name__ == "__main__":
    main()
