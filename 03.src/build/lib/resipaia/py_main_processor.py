import sys
import json
import logging

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def handle_user_check(message_details: dict) -> dict:
    # Placeholder para a lógica de verificação de usuário
    phone_number = message_details.get('from')
    logging.info(f"Chamando py_05_user_registration_logic.py para verificar usuário: {phone_number}")
    # Simula uma resposta
    return {"to": phone_number, "message": f"Verificação de usuário para {phone_number} em andamento. Detalhes: {message_details.get('body')}"}

def handle_reservation(message_details: dict) -> dict:
    # Placeholder para a lógica de reserva
    phone_number = message_details.get('from')
    message_text = message_details.get('body')
    logging.info(f"Chamando py_04_reservation_manager.py para reserva: {phone_number} - {message_text}")
    return {"to": phone_number, "message": f"Processando sua solicitação de reserva: {message_text}"}

def handle_pix_initiation(message_details: dict) -> dict:
    # Placeholder para a lógica de Pix
    phone_number = message_details.get('from')
    message_text = message_details.get('body')
    logging.info(f"Chamando py_01_pix_generator.py para Pix: {phone_number} - {message_text}")
    return {"to": phone_number, "message": f"Iniciando processo Pix: {message_text}"}

def handle_pix_status_check(message_details: dict) -> dict:
    # Placeholder para a lógica de verificação de status Pix
    phone_number = message_details.get('from')
    message_text = message_details.get('body')
    logging.info(f"Chamando py_03_pix_status_checker.py para status Pix: {phone_number} - {message_text}")
    return {"to": phone_number, "message": f"Verificando status Pix: {message_text}"}

def handle_gemini_query(message_details: dict) -> dict:
    # Placeholder para a lógica do Gemini
    phone_number = message_details.get('from')
    message_text = message_details.get('body')
    logging.info(f"Chamando py_02_gemini_supabasedb_interface.py para Gemini: {phone_number} - {message_text}")
    return {"to": phone_number, "message": f"Consultando Gemini para: {message_text}"}

def handle_cancellation(message_details: dict) -> dict:
    # Placeholder para a lógica de cancelamento
    phone_number = message_details.get('from')
    message_text = message_details.get('body')
    logging.info(f"Chamando py_04_reservation_manager.py para cancelamento: {phone_number} - {message_text}")
    return {"to": phone_number, "message": f"Processando seu cancelamento: {message_text}"}

def handle_manage_reservations(message_details: dict) -> dict:
    # Placeholder para a lógica de gerenciamento de reservas
    phone_number = message_details.get('from')
    message_text = message_details.get('body')
    logging.info(f"Chamando py_04_reservation_manager.py para gerenciamento: {phone_number} - {message_text}")
    return {"to": phone_number, "message": f"Gerenciando suas reservas: {message_text}"}

def process_message(message_details: dict) -> dict:
    from_full = message_details.get('from', '')
    if '@c.us' in from_full:
        from_number = from_full.split('@c.us')[0]
    else:
        from_number = from_full
    
    message_details['from'] = from_number # Atualiza o 'from' com o número limpo

    # Garante que 'body' e 'text' existam
    message_details['body'] = message_details.get('body') or message_details.get('text') or ""
    message_details['text'] = message_details.get('text') or message_details.get('body') or ""

    message_text_lower = message_details["body"].lower()

    response = {}

    if not from_number:
        response = {"to": "error", "message": "Número de telefone do remetente não encontrado."}
    else:
        # Lógica de roteamento baseada na intenção
        if message_text_lower == "status pix":
            response = handle_pix_status_check(message_details)
        elif message_text_lower == "gerenciar reservas" or message_text_lower == "minhas reservas":
            response = handle_manage_reservations(message_details)
        elif message_text_lower == "olá" or message_text_lower == "oi" or message_text_lower == "começar":
            response = handle_user_check(message_details)
        elif message_text_lower == "reservar":
            response = handle_reservation(message_details)
        elif message_text_lower == "pix":
            response = handle_pix_initiation(message_details)
        elif message_text_lower == "cancelar":
            response = handle_cancellation(message_details)
        elif message_text_lower == "cadastrar":
            response = handle_user_check(message_details) # Reutiliza para cadastro inicial
        else:
            # Se nenhuma intenção específica for detectada, encaminha para o Gemini
            response = handle_gemini_query(message_details)
    return response

def main():
    if len(sys.argv) > 1:
        n8n_input_str = sys.argv[1]
        try:
            n8n_input = json.loads(n8n_input_str)
            
            # Valida a estrutura do JSON de entrada do n8n
            if not isinstance(n8n_input, list) or not n8n_input or 'json' not in n8n_input[0]:
                raise ValueError("Estrutura do JSON de entrada inválida.")

            message_details = n8n_input[0]['json']
            response = process_message(message_details)
            print(json.dumps(response))

        except (json.JSONDecodeError, ValueError) as e:
            logging.error(f"Erro ao processar a entrada do n8n: {e}")
            print(json.dumps({"to": "error", "message": f"Erro interno ao processar a mensagem: {e}"}))
        except Exception as e:
            logging.error(f"Erro inesperado no py_main_processor: {e}")
            print(json.dumps({"to": "error", "message": f"Ocorreu um erro inesperado: {e}"}))
    else:
        logging.warning("Nenhum argumento fornecido para py_main_processor.py")
        print(json.dumps({"to": "error", "message": "Nenhum argumento fornecido."}))
