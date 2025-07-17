import sys
import json
import logging
from supabase import Client
from resipa.A_db.db_00_supabase_config import get_supabase_client

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_pix(supabase_client: Client, message_details: dict) -> dict:
    # Placeholder para a lógica real de geração de Pix (integração com API de pagamento)
    logging.info(f"Gerando Pix com detalhes: {message_details}")
    
    # Extrai dados relevantes dos detalhes da mensagem
    amount = message_details.get("amount", 0) # Assumindo que o valor virá nos detalhes
    description = message_details.get("description", "Reserva") # Assumindo descrição
    reservation_id = message_details.get("reservation_id", "GENERIC") # Assumindo ID da reserva
    
    txid = f"TXID_{reservation_id}_{amount}"
    qr_code_url = f"https://example.com/qrcode/{txid}"
    pix_link = f"https://example.com/pix/{txid}"

    return {
        "status": "success",
        "txid": txid,
        "qr_code_url": qr_code_url,
        "pix_link": pix_link,
        "message": f"Pix gerado com sucesso! Valor: R${amount:.2f}. Escaneie o QR Code ou use o link: {pix_link}"
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
