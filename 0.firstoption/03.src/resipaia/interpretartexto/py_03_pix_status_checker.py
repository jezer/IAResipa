import sys
import json
import logging
from supabase import Client
from ..A_db.db_00_supabase_config import get_supabase_client

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def update_pix_status(supabase_client: Client, message_details: dict) -> dict:
    txid = message_details.get('txid')
    status = message_details.get('status')
    logging.info(f"Simulando atualização de status do Pix {txid} para {status}. Integração desativada.")
    return {
        "status": "error",
        "code": "PIX_INTEGRATION_DISABLED",
        "message": f"A atualização do status do Pix {txid} está temporariamente desativada. Status solicitado: {status}.",
        "details": {
            "txid": txid,
            "requested_status": status
        }
    }

def check_pix_status(supabase_client: Client, message_details: dict) -> dict:
    txid = message_details.get('txid')
    logging.info(f"Simulando verificação de status do Pix {txid}. Integração desativada.")
    return {
        "status": "error",
        "code": "PIX_INTEGRATION_DISABLED",
        "message": f"A verificação do status do Pix {txid} está temporariamente desativada.",
        "details": {
            "txid": txid,
            "current_simulated_status": "pending" # Sempre retorna pendente em simulação
        }
    }

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
