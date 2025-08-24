            
class WahaReceiverTESTEAPENAS:
    def __init__(self):
        processed_text = "Texto de exemplo com a palavra imagem."
        chat_id = ""
        if "imagem" in processed_text.lower():
            logging.info(f"Palavra 'imagem' detectada. Preparando para enviar imagem para {chat_id}.")
            image_url = "https://github.com/devlikeapro/waha/raw/core/examples/waha.jpg"
            try:
                image_response = requests.get(image_url)
                image_response.raise_for_status()
                image_data_base64 = base64.b64encode(image_response.content).decode('utf-8')
                
                response_payload = {
                    "chatId": chat_id,
                    "file": {
                        "data": f"data:image/jpeg;base64,{image_data_base64}", # Formato data URI
                        "type": "image/jpeg",
                        "filename": "waha.jpg"
                    },
                    "caption": "Aqui está uma imagem de exemplo!",
                    "session": "default"
                }
            except requests.exceptions.RequestException as e:
                logging.error(f"Erro ao baixar ou codificar imagem para {chat_id}: {e}")
                response_payload = {
                    "chatId": chat_id,
                    "text": "Desculpe, não consegui enviar a imagem no momento.",
                    "session": "default"
                }