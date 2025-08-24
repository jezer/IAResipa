import sys
import json
import logging
from supabase import Client
from ..A_db.db_00_supabase_config import get_supabase_client

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_pix(supabase_client: Client, message_details: dict) -> dict:
    # Lógica temporária: Pix desativado para integração futura
    logging.info(f"Simulando geração de Pix. Detalhes recebidos: {message_details}")

    return {
        "status": "error",
        "code": "PIX_NOT_INTEGRATED",
        "message": "A integração com o sistema Pix está temporariamente desativada. Por favor, tente novamente mais tarde ou entre em contato com o suporte.",
        "details": {
            "requested_amount": message_details.get("amount", 0),
            "requested_description": message_details.get("description", "Reserva")
        }
    }

def main():
    action = sys.argv[1] if len(sys.argv) > 1 else None
    
    response = {"status": "error", "message": "Ação ou detalhes da mensagem inválidos."}

    if action == "--generate-pix" and len(sys.argv) > 2:
        try:
            message_details = json.loads(sys.argv[2])
            supabase_client = get_supabase_client()
            response = generate_pix(supabase_client, message_details)
        except json.JSONDecodeError:
            response = {"status": "error", "message": "Detalhes da mensagem inválidos (JSON)."}
    
    print(json.dumps(response))

if __name__ == "__main__":
    main()
