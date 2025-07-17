import sys
import json
import logging
from supabase import Client
from ..A_db.db_00_supabase_config import get_supabase_client

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_user(supabase_client: Client, message_details: dict) -> dict:
    phone_number = message_details.get('from')
    logging.info(f"Verificando usuário: {phone_number}")
    try:
        response = supabase_client.table('cadastro_pessoas_fisica').select('id', 'phone_number').eq('phone_number', phone_number).execute()
        if response.data:
            return {"status": "user_found", "message": f"Bem-vindo de volta, {phone_number}!", "user_id": response.data[0]['id']}
        else:
            return {"status": "user_not_found", "message": f"Olá! Parece que você não está cadastrado. Por favor, faça seu cadastro para continuar."}
    except Exception as e:
        logging.error(f"Erro ao verificar usuário: {e}")
        return {"status": "error", "message": str(e)}

def register_user(supabase_client: Client, message_details: dict) -> dict:
    phone_number = message_details.get('from')
    user_data = {
        "phone_number": phone_number,
        "name": message_details.get('name'),
    }
    if message_details.get('email'):
        user_data['email'] = message_details.get('email')
    logging.info(f"Registrando usuário: {phone_number} com dados: {user_data}")
    try:
        response = supabase_client.table('cadastro_pessoas_fisica').insert(user_data).execute()
        if response.data:
            return {"status": "registration_success", "message": f"Usuário {phone_number} cadastrado com sucesso!"}
        else:
            return {"status": "error", "message": "Falha ao registrar usuário."}
    except Exception as e:
        logging.error(f"Erro ao registrar usuário: {e}")
        return {"status": "error", "message": str(e)}

def delete_user(supabase_client: Client, phone_number: str) -> dict:
    logging.info(f"Deletando usuário: {phone_number}")
    try:
        # Primeiro, encontre o user_id para o phone_number
        user_response = supabase_client.table('cadastro_pessoas_fisica').select('id').eq('phone_number', phone_number).execute()
        if not user_response.data:
            return {"status": "error", "message": f"Usuário {phone_number} não encontrado."}
        user_id = user_response.data[0]['id']

        # Deletar reservas e listas de espera associadas ao usuário
        supabase_client.table('reservas').delete().eq('user_id', user_id).execute()
        supabase_client.table('lista_espera').delete().eq('user_id', user_id).execute()

        # Finalmente, deletar o usuário da tabela cadastro_pessoas_fisica
        response = supabase_client.table('cadastro_pessoas_fisica').delete().eq('phone_number', phone_number).execute()
        if response.data:
            return {"status": "deletion_success", "message": f"Usuário {phone_number} e dados associados deletados com sucesso!"}
        else:
            return {"status": "error", "message": "Falha ao deletar usuário."}
    except Exception as e:
        logging.error(f"Erro ao deletar usuário: {e}")
        return {"status": "error", "message": str(e)}

def main():
    action = sys.argv[1] if len(sys.argv) > 1 else None
    
    response = {"status": "error", "message": "Ação ou detalhes da mensagem inválidos."}

    if action == "--check-user" and len(sys.argv) > 2:
        try:
            message_details = json.loads(sys.argv[2])
            supabase_client = get_supabase_client()
            response = check_user(supabase_client, message_details)
        except json.JSONDecodeError:
            response = {"status": "error", "message": "Detalhes da mensagem inválidos (JSON)."}
    elif action == "--register-user" and len(sys.argv) > 2:
        try:
            message_details = json.loads(sys.argv[2])
            supabase_client = get_supabase_client()
            response = register_user(supabase_client, message_details)
        except json.JSONDecodeError:
            response = {"status": "error", "message": "Detalhes da mensagem inválidos (JSON)."}
    
    print(json.dumps(response))

if __name__ == "__main__":
    main()
