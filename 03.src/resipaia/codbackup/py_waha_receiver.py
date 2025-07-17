import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
import uvicorn
import asyncio
import logging
import requests # Adicionado para download de arquivos
import base64 # Adicionado para codificação base64
# from pydub import AudioSegment # Necessário para manipulação de áudio
# import speech_recognition as sr # Necessário para reconhecimento de fala
from resipaia.codbackup.py_main_processor import process_message_logic # Importa a lógica principal

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

class WahaReceiver:
    def __init__(self):
        self.waha_api_url = os.getenv("WAHA_API_URL","http://localhost:3000/api")
        self.host = os.getenv("APP_HOST", "0.0.0.0")
        self.port = int(os.getenv("APP_PORT", 8000))
        self.app = FastAPI()
        self.setup_routes()

    def setup_routes(self):
        @self.app.post("/webhook")
        async def webhook(request: Request):
            return await self.handle_webhook(request)

    async def handle_webhook(self, request: Request):
        # Etapa 1: Resposta imediata
        logging.info("Webhook recebido. Respondendo imediatamente com status 'received'.")
        
        # Inicia o processamento em background
        asyncio.create_task(self.process_message_from_waha(await request.json()))
        
        return {"status": "received"}

# ... (restante do código da classe WahaReceiver)

    def adapt_waha_to_processor_format(self, waha_payload: dict) -> dict:
        """
        Adapta o payload recebido do Waha para o formato esperado por py_main_processor.py.
        """
        # O py_main_processor.py espera um dicionário com 'from' (número limpo) e 'body'/'text'.
        # O 'from' já é limpo dentro do process_message_logic, então passamos o original.
        # O 'body' ou 'text' virá do nosso pré-processamento (texto, áudio, imagem).
        
        # O 'from' do Waha pode vir como '5511999999999@c.us'. O process_message_logic já lida com isso.
        # O 'body' ou 'text' será o texto processado (transcrito/OCR).

        adapted_payload = {
            "from": waha_payload.get("chatId"), # chatId do Waha é o 'from' para o processador
            "body": waha_payload.get("processed_text", ""), # Usar o texto já pré-processado
            "text": waha_payload.get("processed_text", "") # Duplicar para compatibilidade
        }
        return adapted_payload

    async def process_message_from_waha(self, message_details: dict):
        # Extrai o payload real da mensagem
        waha_payload = message_details.get('payload', {})
        
        chat_id = waha_payload.get("from") # O chatId está em 'payload.from'
        message_type = waha_payload.get("type", waha_payload.get('_data', {}).get('Info', {}).get('Type', 'text')) # Tenta pegar o tipo, padrão 'text'
        processed_text = ""

        if chat_id:
            logging.info(f"Processando mensagem de {chat_id} (Tipo: {message_type}).")
            
            if message_type == "text":
                processed_text = waha_payload.get("body", "") or waha_payload.get("text", "")
                logging.info(f"Mensagem de texto recebida: {processed_text}")
            elif message_type == "audio":
                audio_url = waha_payload.get("mediaUrl") or waha_payload.get('media', {}).get('url') # Tenta pegar de mediaUrl ou media.url
                if audio_url:
                    processed_text = await self._transcribe_audio(audio_url)
                else:
                    logging.warning(f"Mensagem de áudio sem URL de mídia para {chat_id}.")
                    processed_text = "Não foi possível transcrever o áudio: URL não fornecida."
            elif message_type == "image":
                image_url = waha_payload.get("mediaUrl") or waha_payload.get('media', {}).get('url') # Tenta pegar de mediaUrl ou media.url
                if image_url:
                    processed_text = await self._ocr_image(image_url)
                else:
                    logging.warning(f"Mensagem de imagem sem URL de mídia para {chat_id}.")
                    processed_text = "Não foi possível extrair texto da imagem: URL não fornecida."
            else:
                logging.warning(f"Tipo de mensagem '{message_type}' não suportado para {chat_id}.")
                processed_text = f"Tipo de mensagem '{message_type}' não suportado."

            # Adiciona o texto processado ao message_details para o adaptador
            # O adaptador espera 'chatId' e 'processed_text' no nível superior
            adapted_message_details = {
                "chatId": chat_id,
                "processed_text": processed_text
            }

            # Etapa 2 (Integração): Chamar o processador principal
            adapted_payload = self.adapt_waha_to_processor_format(adapted_message_details)
            
            # Invoca a lógica principal do processador
            processor_response = process_message_logic(adapted_payload)
            
            # Extrai a mensagem de resposta do processador
            response_message_text = processor_response.get("message", "Erro ao processar a mensagem.")
            logging.info(f"Preparando para enviar mensagem de texto para {chat_id}: {response_message_text}")
            response_payload = {
                "chatId": chat_id,
                "text": response_message_text,
                "session": "default"
            }
            logging.info(f"Enviando resposta final para {chat_id}.")
            session_id = waha_payload.get("session", "default") # Extrai o session_id do payload ou usa 'default'
            await self.send_response_to_waha(response_payload, session_id) # Passa o session_id para o método de envio
        else:
            logging.warning("chatId não encontrado na mensagem recebida (após extração do payload). Ignorando.")

    async def _transcribe_audio(self, audio_url: str) -> str:
        logging.info(f"Iniciando transcrição de áudio para: {audio_url}")
        try:
            # --- Lógica para download e transcrição de áudio (requer bibliotecas como requests, pydub, speech_recognition) ---
            # Exemplo de download (descomente e instale 'requests' se for usar):
            # response = requests.get(audio_url, stream=True)
            # response.raise_for_status()
            # with open("temp_audio.ogg", "wb") as f:
            #     for chunk in response.iter_content(chunk_size=8192):
            #         f.write(chunk)
            # logging.info("Áudio baixado para temp_audio.ogg")

            # Exemplo de transcrição (descomente e instale 'speech_recognition' e um backend como 'Whisper' se for usar):
            # r = sr.Recognizer()
            # with sr.AudioFile("temp_audio.ogg") as source:
            #     audio_data = r.record(source)
            #     text = r.recognize_whisper(audio_data) # Ou recognize_google, etc.
            # logging.info(f"Áudio transcrito: {text}")
            # return text
            
            # Placeholder para simular a transcrição
            return f"Texto transcrito do áudio de {audio_url} (simulado)."
        except Exception as e:
            logging.error(f"Erro ao transcrever áudio de {audio_url}: {e}")
            return "Erro na transcrição do áudio."

    async def _ocr_image(self, image_url: str) -> str:
        logging.info(f"Iniciando OCR em imagem de: {image_url}")
        try:
            # --- Lógica para download e OCR de imagem (requer bibliotecas como requests, Pillow, pytesseract) ---
            # Exemplo de download (descomente e instale 'requests' se for usar):
            # response = requests.get(image_url, stream=True)
            # response.raise_for_status()
            # with open("temp_image.png", "wb") as f:
            #     for chunk in response.iter_content(chunk_size=8192):
            #         f.write(chunk)
            # logging.info("Imagem baixada para temp_image.png")

            # Exemplo de OCR (descomente e instale 'Pillow' e 'pytesseract' se for usar):
            # from PIL import Image
            # import pytesseract
            # text = pytesseract.image_to_string(Image.open("temp_image.png"))
            # logging.info(f"Texto extraído da imagem: {text}")
            # return text

            # Placeholder para simular o OCR
            return f"Texto extraído da imagem de {image_url} (simulado)."
        except Exception as e:
            logging.error(f"Erro ao realizar OCR em imagem de {image_url}: {e}")
            return "Erro na extração de texto da imagem."

    async def send_response_to_waha(self, message_payload: dict, session_id: str):
        logging.info(f"Enviando payload para Waha: {message_payload}")
        try:
            # Determina se é uma mensagem de texto ou um arquivo
            if "file" in message_payload:
                endpoint = "/sendMedia" # Endpoint correto para envio de mídia, sem /api duplicado
                message_payload["sessionId"] = session_id # Adiciona sessionId ao payload
            else:
                endpoint = "/sendText" # Endpoint para texto, sem /api duplicado

            response = requests.post(f"{self.waha_api_url}{endpoint}", json=message_payload)
            response.raise_for_status() # Levanta um erro para status HTTP ruins (4xx ou 5xx)
            logging.info(f"Resposta enviada com sucesso para Waha. Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao enviar resposta para Waha via API: {e}")

    def start_server(self):
        logging.info(f"Iniciando servidor FastAPI em http://{self.host}:{self.port}")
        uvicorn.run(self.app, host=self.host, port=self.port)

if __name__ == "__main__":
    receiver = WahaReceiver()
    receiver.start_server()
