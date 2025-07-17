import sys
import json
import logging
from supabase import Client
from resipaia.A_db.db_00_supabase_config import get_supabase_client

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_active_reservations(supabase_client: Client, message_details: dict) -> dict:
    user_id = message_details.get('user_id')
    logging.info(f"Verificando reservas ativas para: {user_id}")
    try:
        response = supabase_client.table('reservas').select('*').eq('user_id', user_id).eq('status', 'ativa').execute()
        if response.data:
            return {"status": "active_reservations_found", "reservations": response.data, "message": f"Você possui {len(response.data)} reservas ativas."}
        else:
            return {"status": "no_active_reservations", "message": "Você não possui reservas ativas no momento."}
    except Exception as e:
        logging.error(f"Erro ao verificar reservas ativas: {e}")
        return {"status": "error", "message": str(e)}

def check_availability(supabase_client: Client, message_details: dict) -> dict:
    resource_type = message_details.get('resource_type')
    logging.info(f"Consultando disponibilidade para: {resource_type}")
    try:
        # Exemplo simplificado: buscar recursos disponíveis
        response = supabase_client.table('recursos').select('*').eq('is_available', True).eq('type', resource_type).execute()
        if response.data:
            options = [f"{r['name']} ({r['type']})" for r in response.data]
            return {"status": "available", "options": options, "message": "Opções disponíveis: " + ", ".join(options)}
        else:
            return {"status": "not_available", "message": "Nenhum recurso disponível no momento."}
    except Exception as e:
        logging.error(f"Erro ao consultar disponibilidade: {e}")
        return {"status": "error", "message": str(e)}

def create_provisional_reservation(supabase_client: Client, message_details: dict) -> dict:
    logging.info(f"Criando reserva provisória com detalhes: {message_details}")
    try:
        # Assumindo que message_details contém user_id, resource_id, start_time, end_time, amount
        reservation_data = {
            "user_id": message_details.get('user_id'),
            "resource_id": message_details.get('resource_id'),
            "start_time": message_details.get('start_time'),
            "end_time": message_details.get('end_time'),
            "status": "provisoria",
            "pix_txid": message_details.get('pix_txid'),
            "amount": message_details.get('amount')
        }
        response = supabase_client.table('reservas').insert(reservation_data).execute()
        if response.data:
            return {"status": "provisional_created", "reservation_id": response.data[0]['id'], "message": "Sua reserva provisória foi criada com sucesso!"}
        else:
            return {"status": "error", "message": "Falha ao criar reserva provisória."}
    except Exception as e:
        logging.error(f"Erro ao criar reserva provisória: {e}")
        return {"status": "error", "message": str(e)}

def manage_existing_reservations(supabase_client: Client, message_details: dict) -> dict:
    user_id = message_details.get('user_id')
    action = message_details.get('action', 'view')
    reservation_id = message_details.get('reservation_id')
    new_data = message_details.get('new_data')

    logging.info(f"Gerenciando reservas para {user_id}: Ação={action}, ID={reservation_id}, Dados={new_data}")
    try:
        if action == "view":
            response = supabase_client.table('reservas').select('*').eq('user_id', user_id).execute()
            if response.data:
                return {"status": "success", "reservations": response.data, "message": "Suas reservas:"}
            else:
                return {"status": "no_reservations", "message": "Você não possui reservas."}
        elif action == "cancel":
            response = supabase_client.table('reservas').update({'status': 'cancelada'}).eq('id', reservation_id).execute()
            if response.data:
                return {"status": "success", "message": f"Reserva {reservation_id} cancelada com sucesso."}
            else:
                return {"status": "error", "message": f"Falha ao cancelar reserva {reservation_id}."}
        elif action == "modify":
            response = supabase_client.table('reservas').update(new_data).eq('id', reservation_id).execute()
            if response.data:
                return {"status": "success", "message": f"Reserva {reservation_id} modificada com sucesso."}
            else:
                return {"status": "error", "message": f"Falha ao modificar reserva {reservation_id}."}
        else:
            return {"status": "error", "message": "Ação de gerenciamento de reserva inválida."}
    except Exception as e:
        logging.error(f"Erro ao gerenciar reservas: {e}")
        return {"status": "error", "message": str(e)}

def add_to_waiting_list(supabase_client: Client, message_details: dict) -> dict:
    logging.info(f"Adicionando à lista de espera com detalhes: {message_details}")
    try:
        # Assumindo que message_details contém user_id, resource_id, requested_time
        waiting_data = {
            "user_id": message_details.get('user_id'),
            "resource_id": message_details.get('resource_id'),
            "requested_time": message_details.get('requested_time'),
            "status": "pendente"
        }
        response = supabase_client.table('lista_espera').insert(waiting_data).execute()
        if response.data:
            return {"status": "added_to_waiting_list", "waiting_id": response.data[0]['id'], "message": "Você foi adicionado à lista de espera."}
        else:
            return {"status": "error", "message": "Falha ao adicionar à lista de espera."}
    except Exception as e:
        logging.error(f"Erro ao adicionar à lista de espera: {e}")
        return {"status": "error", "message": str(e)}

def notify_waiting_list(supabase_client: Client, resource_id: str) -> dict:
    logging.info(f"Notificando lista de espera para recurso: {resource_id}")
    try:
        # Buscar usuários na lista de espera para este recurso
        response = supabase_client.table('lista_espera').select('*').eq('resource_id', resource_id).eq('status', 'pendente').execute()
        if response.data:
            notified_users = [item['user_id'] for item in response.data]
            # Simular envio de notificação (na vida real, chamaria uma API de mensagem)
            return {"status": "notification_sent", "notified_users": notified_users, "message": f"Notificação enviada para {len(notified_users)} usuários na lista de espera."}
        else:
            return {"status": "no_waiting_users", "message": "Nenhum usuário na lista de espera para este recurso."}
    except Exception as e:
        logging.error(f"Erro ao notificar lista de espera: {e}")
        return {"status": "error", "message": str(e)}

def main():
    action = sys.argv[1] if len(sys.argv) > 1 else None
    
    response = {"status": "error", "message": "Ação ou detalhes da mensagem inválidos."}

    if action == "--check-active-reservations" and len(sys.argv) > 2:
        try:
            message_details = json.loads(sys.argv[2])
            supabase_client = get_supabase_client()
            response = check_active_reservations(supabase_client, message_details)
        except json.JSONDecodeError:
            response = {"status": "error", "message": "Detalhes da mensagem inválidos (JSON)."}
    elif action == "--check-availability" and len(sys.argv) > 2:
        try:
            message_details = json.loads(sys.argv[2])
            supabase_client = get_supabase_client()
            response = check_availability(supabase_client, message_details)
        except json.JSONDecodeError:
            response = {"status": "error", "message": "Detalhes da mensagem inválidos (JSON)."}
    elif action == "--create-provisional-reservation" and len(sys.argv) > 2:
        try:
            message_details = json.loads(sys.argv[2])
            supabase_client = get_supabase_client()
            response = create_provisional_reservation(supabase_client, message_details)
        except json.JSONDecodeError:
            response = {"status": "error", "message": "Detalhes da mensagem inválidos (JSON)."}
    elif action == "--manage-existing-reservations" and len(sys.argv) > 2:
        try:
            message_details = json.loads(sys.argv[2])
            supabase_client = get_supabase_client()
            response = manage_existing_reservations(supabase_client, message_details)
        except json.JSONDecodeError:
            response = {"status": "error", "message": "Detalhes da mensagem inválidos (JSON)."}
    elif action == "--add-to-waiting-list" and len(sys.argv) > 2:
        try:
            message_details = json.loads(sys.argv[2])
            supabase_client = get_supabase_client()
            response = add_to_waiting_list(supabase_client, message_details)
        except json.JSONDecodeError:
            response = {"status": "error", "message": "Detalhes da mensagem inválidos (JSON)."}
    elif action == "--notify-waiting-list" and len(sys.argv) > 2:
        # notify_waiting_list ainda espera resource_id como string, não message_details
        # Isso precisaria ser ajustado se a intenção for passar message_details para todas as funções
        resource_id = sys.argv[2] # Temporariamente mantendo como string
        supabase_client = get_supabase_client()
        response = notify_waiting_list(supabase_client, resource_id)
    
    print(json.dumps(response))

if __name__ == "__main__":
    main()
