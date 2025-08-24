import sys
import json
import logging
from supabase import Client
from resipa.A_db.db_00_supabase_config import get_supabase_client

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def update_pix_status(supabase_client: Client, message_details: dict) -> dict:
    txid = message_details.get('txid')
    status = message_details.get('status')
    logging.info(f"Atualizando status do Pix {txid} para {status}")
    
    try:
        response = supabase_client.table('reservas').update({'status': status}).eq('pix_txid', txid).execute()
        if response.data:
            return {"status": "success", "message": f"Pagamento Pix {txid} confirmado e reserva finalizada!"}
        else:
            return {"status": "error", "message": f"Reserva com TXID {txid} não encontrada ou não atualizada."}
    except Exception as e:
        logging.error(f"Erro ao atualizar status do Pix {txid}: {e}")
        return {"status": "error", "message": str(e)}

def check_pix_status(supabase_client: Client, message_details: dict) -> dict:
    txid = message_details.get('txid')
    logging.info(f"Verificando status do Pix {txid}")
    
    try:
        response = supabase_client.table('reservas').select('status').eq('pix_txid', txid).single().execute()
        if response.data:
            current_status = response.data['status']
            return {"status": "success", "txid": txid, "current_status": current_status, "message": f"O Pix {txid} está com status: {current_status}."}
        else:
            return {"status": "error", "message": f"Reserva com TXID {txid} não encontrada."}
    except Exception as e:
        logging.error(f"Erro ao verificar status do Pix {txid}: {e}")
        return {"status": "error", "message": str(e)}

def main():
    action = sys.argv[1] if len(sys.argv) > 1 else None
    
    response = {"status": "error", "message": "Ação ou detalhes da mensagem inválidos."}

    if action == "--update-status" and len(sys.argv) > 2:
        try:
            message_details = json.loads(sys.argv[2])
            supabase_client = get_supabase_client()
            response = update_pix_status(supabase_client, message_details)
        except json.JSONDecodeError:
            response = {"status": "error", "message": "Detalhes da mensagem inválidos (JSON)."}
    elif action == "--check-status" and len(sys.argv) > 2:
        try:
            message_details = json.loads(sys.argv[2])
            supabase_client = get_supabase_client()
            response = check_pix_status(supabase_client, message_details)
        except json.JSONDecodeError:
            response = {"status": "error", "message": "Detalhes da mensagem inválidos (JSON)."}
    
    print(json.dumps(response))

if __name__ == "__main__":
    main()
