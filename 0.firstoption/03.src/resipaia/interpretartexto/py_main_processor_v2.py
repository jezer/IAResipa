import sys
import json
import logging
import requests # Adicionado para download de arquivos
import base64 # Adicionado para codificação base64
from datetime import datetime, timedelta # Adicionado para gerar timestamps únicos
import uuid # Adicionado para gerar UUIDs
from .py_05_user_registration_logic import check_user, register_user, delete_user
from .py_04_reservation_manager import check_active_reservations, check_availability, create_provisional_reservation, manage_existing_reservations, add_to_waiting_list, notify_waiting_list
from .py_01_pix_generator import generate_pix
from .py_03_pix_status_checker import check_pix_status, update_pix_status
from resipaia.A_db.db_00_supabase_config import get_supabase_client

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configurações da API Gemini
API_KEY = "AIzaSyBbR52zZ37OlDXtNjWS_Nq85QXXG7E_hMw" # Substitua pela sua chave de API real
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"

def gerar_resposta_gemini(contexto: str, mensagem_usuario: str, temperature: float = 0.7, max_tokens: int = 512):
    """
    Envia um payload para a API Gemini e retorna o texto gerado.
    """
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"Contexto: {contexto}\nUsuário: {mensagem_usuario}"}
                ]
            }
        ],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_tokens
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        resp = requests.post(ENDPOINT, headers=headers, data=json.dumps(payload))
        resp.raise_for_status()
        resposta_json = resp.json()
        if "candidates" in resposta_json and len(resposta_json["candidates"]) > 0:
            return resposta_json["candidates"][0]["content"]
        else:
            logging.warning(f"Resposta do Gemini não contém 'candidates': {resposta_json}")
            return "Desculpe, não consegui gerar uma resposta no momento."
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao chamar a API Gemini: {e}")
        return "Desculpe, houve um erro ao processar sua solicitação com o Gemini."










def handle_user_check(message_details: dict) -> dict:
    phone_number = message_details.get('from')
    message_text = message_details.get('body', '')
    logging.info(f"Processando verificação/cadastro para usuário: {phone_number}")
    
    supabase_client = get_supabase_client()
    
    # Tenta extrair o número a ser cadastrado se a mensagem começar com "cadastrar"
    new_user_phone = None
    if message_text.lower().startswith("cadastrar "):
        parts = message_text.split(" ", 1)
        if len(parts) > 1:
            new_user_phone = parts[1].strip()
            # Validação simples do número de telefone
            if not new_user_phone.isdigit() or len(new_user_phone) < 10: # Exemplo de validação
                return {"to": phone_number, "status": "error", "raw_message": "Número de telefone inválido para cadastro. Por favor, forneça um número válido."}

    # Se um novo número foi fornecido (admin tentando cadastrar)
    if new_user_phone:
        # Aqui você precisaria de uma lógica para verificar se o 'phone_number' atual é de um admin
        # Por enquanto, vamos simular que qualquer um pode cadastrar para fins de teste.
        # Em produção, você consultaria uma tabela de admins ou usaria autenticação.
        logging.info(f"Tentativa de cadastro de novo usuário: {new_user_phone} por {phone_number}")
        register_details = {"from": new_user_phone, "name": "Novo Usuário"} # Pode adicionar mais detalhes
        registration_response = register_user(supabase_client, register_details)
        
        if registration_response["status"] == "registration_success":
            return {"to": phone_number, "status": "success", "raw_message": f"Usuário {new_user_phone} cadastrado com sucesso!"}
        else:
            return {"to": phone_number, "status": "error", "raw_message": f"Falha ao cadastrar usuário {new_user_phone}: {registration_response.get('message', 'Erro desconhecido')}"}
    else:
        # Se não é uma tentativa de cadastro, verifica o usuário atual
        user_check_response = check_user(supabase_client, message_details)
        
        if user_check_response["status"] == "user_found":
            message_details["user_id"] = user_check_response["user_id"] # Adiciona o user_id (UUID) ao message_details
            return {"to": phone_number, "status": "user_found", "raw_message": user_check_response["message"] + " Como posso ajudar hoje?"}
        elif user_check_response["status"] == "user_not_found":
            return {"to": phone_number, "status": "user_not_found", "raw_message": "Olá! Parece que você não está cadastrado. Para se cadastrar, digite 'cadastrar' seguido do seu nome."}
        else:
            return {"to": phone_number, "status": "error", "raw_message": f"Erro ao verificar usuário: {user_check_response.get('message', 'Erro desconhecido')}"}

def handle_reservation(message_details: dict) -> dict:
    phone_number = message_details.get('from')
    message_text = message_details.get('body', '').lower()
    logging.info(f"Processando solicitação de reserva para: {phone_number} - {message_text}")

    supabase_client = get_supabase_client()

    if "reservas ativas" in message_text or "minhas reservas" in message_text:
        response = check_active_reservations(supabase_client, message_details)
        # Garantir que check_active_reservations retorna 'status'
        if "status" not in response:
            response["status"] = "info" # Default status if missing
        return response

    elif "disponibilidade" in message_text or "opções disponíveis" in message_text:
        response = check_availability(supabase_client, message_details)
        # Garantir que check_availability retorna 'status'
        if "status" not in response:
            response["status"] = "info" # Default status if missing
        return response

    elif "reservar" in message_text:
        # Simular a criação de reserva provisória sem interagir com o DB real
        # Para testes, vamos retornar uma resposta fixa e controlada.
        logging.info(f"Simulando criação de reserva provisória para: {phone_number}")
        return {
            "to": phone_number,
            "status": "info",
            "raw_message": "Sua solicitação de reserva foi recebida e está sendo processada (simulado). Em breve você receberá os detalhes para pagamento."
        }

    elif "lista de espera" in message_text:
        # Simular adição à lista de espera sem interagir com o DB real
        logging.info(f"Simulando adição à lista de espera para: {phone_number}")
        return {
            "to": phone_number,
            "status": "info",
            "raw_message": "Você foi adicionado à lista de espera (simulado). Notificaremos quando houver disponibilidade."
        }

    else:
        return {"to": phone_number, "status": "error", "raw_message": "Não entendi sua solicitação de reserva. Por favor, tente novamente com mais detalhes."}

def handle_pix_initiation(message_details: dict) -> dict:
    phone_number = message_details.get('from')
    logging.info(f"Iniciando processo de geração de Pix para: {phone_number}")
    supabase_client = get_supabase_client()
    pix_response = generate_pix(supabase_client, message_details)
    # Garantir que pix_response tem 'status'
    if "status" not in pix_response:
        pix_response["status"] = "error" # Default to error if not present
    return {"to": phone_number, "status": pix_response["status"], "raw_message": pix_response.get("message", "Erro ao gerar Pix.")}

def handle_pix_status_check(message_details: dict) -> dict:
    phone_number = message_details.get('from')
    logging.info(f"Verificando status do Pix para: {phone_number}")
    supabase_client = get_supabase_client()
    pix_status_response = check_pix_status(supabase_client, message_details)
    # Garantir que pix_status_response tem 'status'
    if "status" not in pix_status_response:
        pix_status_response["status"] = "error" # Default to error if not present
    return {"to": phone_number, "status": pix_status_response["status"], "raw_message": pix_status_response.get("message", "Erro ao verificar status do Pix.")}

def handle_gemini_query(message_details: dict, context_for_gemini: str = "") -> dict:
    phone_number = message_details.get('from')
    prompt = message_details.get('body')
    logging.info(f"Consultando Gemini com prompt: {prompt}")

    # Combine o prompt do usuário com qualquer contexto adicional
    full_prompt = f"{context_for_gemini}\n\n{prompt}" if context_for_gemini else prompt

    gemini_response = gerar_resposta_gemini(
        contexto="Você é um assistente de reservas de WhatsApp. Responda de forma amigável, formal e útil.",
        mensagem_usuario=full_prompt
    )
    return {"to": phone_number, "status": "success", "message": gemini_response["parts"][0]["text"]}

def handle_cancellation(message_details: dict) -> dict:
    phone_number = message_details.get('from')
    message_text = message_details.get('body')
    logging.info(f"Processando cancelamento para: {phone_number} - {message_text}")
    # Simular cancelamento
    reservation_id = message_text.lower().replace("cancelar ", "")
    return {"to": phone_number, "status": "success", "raw_message": f"Reserva {reservation_id} cancelada com sucesso."}

def handle_manage_reservations(message_details: dict) -> dict:
    phone_number = message_details.get('from')
    message_text = message_details.get('body')
    logging.info(f"Gerenciando reservas para {phone_number}: {message_text}")

    supabase_client = get_supabase_client()

    # Simulação de gerenciamento de reservas
    if "modificar" in message_text.lower():
        # Simular modificação
        # Extrai o reservation_id da message_text
        # Exemplo message_text: "gerenciar reservas modificar res_active_002 nova data 2025-08-01"
        parts = message_text.lower().split(' ')
        # O ID da reserva é a 4ª palavra (índice 3)
        reservation_id = parts[3] if len(parts) > 3 else "UNKNOWN_ID"
        return {"to": phone_number, "status": "success", "raw_message": f"Reserva {reservation_id} modificada com sucesso (simulado)."}
    elif "cancelar" in message_text.lower():
        # Simular cancelamento
        reservation_id = message_text.lower().replace("cancelar ", "")
        return {"to": phone_number, "status": "success", "raw_message": f"Reserva {reservation_id} cancelada com sucesso (simulado)."}
    elif "minhas reservas" in message_text.lower() or "gerenciar reservas" in message_text.lower():
        # Simular retorno de reservas (vazio ou com dados de teste)
        return {"to": phone_number, "status": "success", "raw_message": "Suas reservas: (simulado)", "reservations": []}
    else:
        return {"to": phone_number, "status": "error", "raw_message": "Não entendi sua solicitação de gerenciamento de reservas."}

def handle_user_removal(message_details: dict) -> dict:
    phone_number_to_delete = message_details.get('body', '').lower().replace("remover usuario ", "")
    admin_phone_number = message_details.get('from')
    logging.info(f"Tentativa de remoção de usuário: {phone_number_to_delete} por admin: {admin_phone_number}")

    supabase_client = get_supabase_client()

    if phone_number_to_delete:
        delete_response = delete_user(supabase_client, phone_number_to_delete)
        if delete_response["status"] == "deletion_success":
            return {"to": admin_phone_number, "status": "success", "raw_message": f"Usuário {phone_number_to_delete} removido com sucesso!"}
        else:
            return {"to": admin_phone_number, "status": "error", "raw_message": f"Falha ao remover usuário {phone_number_to_delete}: {delete_response.get('message', 'Erro desconhecido')}"}
    else:
        return {"to": admin_phone_number, "status": "error", "raw_message": "Comando de remoção de usuário inválido. Use 'remover usuario [numero]'."}

def process_message_logic(message_details: dict) -> dict:
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
    raw_message_for_gemini = ""

    if not from_number:
        response = {"to": "error", "message": "Número de telefone do remetente não encontrado."}
    else:
        # Lógica de roteamento baseada na intenção
        if message_text_lower == "status pix":
            response = handle_pix_status_check(message_details)
        elif message_text_lower.startswith("gerenciar reservas") or message_text_lower == "minhas reservas":
            response = handle_manage_reservations(message_details)
        elif message_text_lower == "olá" or message_text_lower == "oi" or message_text_lower == "começar":
            response = handle_user_check(message_details)
        elif message_text_lower.startswith("reservar") or message_text_lower.startswith("disponibilidade") or message_text_lower.startswith("lista de espera") or message_text_lower.startswith("agendar"):
            response = handle_reservation(message_details)
        elif message_text_lower == "pix":
            response = handle_pix_initiation(message_details)
        elif message_text_lower.startswith("cancelar"):
            response = handle_cancellation(message_details)
        elif message_text_lower.startswith("remover usuario"):
            response = handle_user_removal(message_details)
        elif message_text_lower.startswith("cadastrar"):
            response = handle_user_check(message_details)
        else:
            # Se nenhuma intenção específica for detectada, encaminha para o Gemini diretamente
            response = handle_gemini_query(message_details)
            return response # Retorna diretamente pois handle_gemini_query já formata a mensagem

    # Se a resposta de uma função handle_* contém uma raw_message, use o Gemini para formatá-la
    if "raw_message" in response:
        raw_message_for_gemini = response.pop("raw_message") # Remove raw_message do response
        logging.info(f"message_details: {message_details}, raw_message_for_gemini: {raw_message_for_gemini}.")
        gemini_formatted_response = handle_gemini_query(message_details, context_for_gemini=raw_message_for_gemini)
        response["message"] = gemini_formatted_response["message"]["parts"][0]["text"] # Atualiza a mensagem com a resposta do Gemini
        response["status"] = gemini_formatted_response["status"] # Atualiza o status com a resposta do Gemini

    # Lógica para responder com imagem se a palavra "imagem" estiver no texto processado
    if "imagem" in message_text_lower:
        logging.info(f"Palavra 'imagem' detectada. Preparando para enviar imagem para {from_number}.")
        image_url = "https://github.com/devlikeapro/waha/raw/core/examples/waha.jpg"
        try:
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            image_data_base64 = base64.b64encode(image_response.content).decode('utf-8')
            
            response = {
                "to": from_number,
                "status": "success",
                "file": {
                    "data": f"data:image/jpeg;base64,{image_data_base64}",
                    "type": "image/jpeg",
                    "filename": "waha.jpg"
                },
                "caption": "Aqui está uma imagem de exemplo!",
                "session": "default"
            }
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao baixar ou codificar imagem para {from_number}: {e}")
            response = {
                "to": from_number,
                "status": "error",
                "message": "Desculpe, não consegui enviar a imagem no momento.",
                "session": "default"
            }

    return response


