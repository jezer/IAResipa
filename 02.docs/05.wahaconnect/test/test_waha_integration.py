import pytest
import requests
import threading
import time
import uvicorn
import asyncio
from fastapi import FastAPI, Request
from typing import Dict, List
from unittest.mock import MagicMock

# Mock da API do Waha para capturar respostas
mock_waha_app = FastAPI()
received_responses: List[Dict] = []
responses_lock = threading.Lock()

@mock_waha_app.post("/sendText")
async def mock_send_text(request: Request):
    data = await request.json()
    with responses_lock:
        received_responses.append(data)
    return {"status": "success"}

@mock_waha_app.get("/_clear_responses")
async def clear_responses():
    with responses_lock:
        received_responses.clear()
    return {"status": "cleared"}

@mock_waha_app.get("/_get_responses")
async def get_responses():
    with responses_lock:
        return {"responses": list(received_responses)}

def run_mock_waha_api():
    uvicorn.run(mock_waha_app, host="127.0.0.1", port=8001, log_level="warning")

# --- Testes de Integração para WahaReceiver ---

# Fixture para iniciar o mock da API do Waha
@pytest.fixture(scope="module")
def mock_waha_api_server():
    thread = threading.Thread(target=run_mock_waha_api, daemon=True)
    thread.start()
    time.sleep(1)  # Give the server a moment to start
    yield
    # No teardown needed as it's a daemon thread and will exit with the main program

# Fixture para iniciar o WahaReceiver
@pytest.fixture(scope="module")
def waha_receiver_server():
    import os
    os.environ["WAHA_API_URL"] = "http://127.0.0.1:8001"
    os.environ["APP_HOST"] = "127.0.0.1"
    os.environ["APP_PORT"] = "8000"

    from resipaia.codbackup.py_waha_receiver import WahaReceiver

    receiver = WahaReceiver()
    
    server_thread = threading.Thread(target=receiver.start_server, daemon=True)
    server_thread.start()
    time.sleep(2) # Give the server a moment to start
    yield

@pytest.fixture(autouse=True)
def clear_mock_responses():
    requests.get("http://127.0.0.1:8001/_clear_responses")
    yield

@pytest.fixture
def mock_process_message_logic(monkeypatch):
    mock = MagicMock(return_value={"to": "mock_user", "message": "Resposta mockada do processador."})
    monkeypatch.setattr("resipaia.py_main_processor.process_message_logic", mock)
    return mock

def send_webhook_request(payload: Dict):
    url = "http://127.0.0.1:8000/webhook"
    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar requisição: {e}")
        return None

@pytest.mark.asyncio
async def test_integration_text_message(mock_waha_api_server, waha_receiver_server, mock_process_message_logic):
    chat_id = "user_text@c.us"
    text_message_payload = {
        "event": "message",
        "chatId": chat_id,
        "type": "text",
        "body": "Olá, como posso ajudar?"
    }
    
    # Configura o mock para retornar uma resposta específica para este teste
    mock_process_message_logic.return_value = {"to": chat_id, "message": "Texto processado com sucesso!"}

    response = send_webhook_request(text_message_payload)
    assert response == {"status": "received"}

    await asyncio.sleep(1) # Aguarda o processamento em background

    # Verifica se process_message_logic foi chamado corretamente
    mock_process_message_logic.assert_called_once()
    called_args = mock_process_message_logic.call_args[0][0]
    assert called_args["from"] == chat_id.split('@')[0] # O processador limpa o @c.us
    assert called_args["body"] == "Olá, como posso ajudar?"

    # Verifica a resposta enviada ao Waha
    response_data = requests.get("http://127.0.0.1:8001/_get_responses").json()
    assert len(response_data["responses"]) == 1
    assert response_data["responses"][0]["chatId"] == chat_id
    assert response_data["responses"][0]["text"] == "Texto processado com sucesso!"

@pytest.mark.asyncio
async def test_integration_audio_message(mock_waha_api_server, waha_receiver_server, mock_process_message_logic, monkeypatch):
    chat_id = "user_audio@c.us"
    audio_url = "http://localhost:3000/media/audio_test.ogg"
    audio_message_payload = {
        "event": "message",
        "chatId": chat_id,
        "type": "audio",
        "mediaUrl": audio_url
    }

    # Mock do _transcribe_audio para simular a transcrição
    mock_transcribe = MagicMock(return_value="Este é um texto de áudio transcrito.")
    monkeypatch.setattr("resipaia.py_waha_receiver.WahaReceiver._transcribe_audio", mock_transcribe)

    mock_process_message_logic.return_value = {"to": chat_id, "message": "Áudio processado com sucesso!"}

    response = send_webhook_request(audio_message_payload)
    assert response == {"status": "received"}

    await asyncio.sleep(1) # Aguarda o processamento em background

    mock_transcribe.assert_called_once_with(audio_url)
    mock_process_message_logic.assert_called_once()
    called_args = mock_process_message_logic.call_args[0][0]
    assert called_args["body"] == "Este é um texto de áudio transcrito."

    response_data = requests.get("http://127.0.0.1:8001/_get_responses").json()
    assert len(response_data["responses"]) == 1
    assert response_data["responses"][0]["chatId"] == chat_id
    assert response_data["responses"][0]["text"] == "Áudio processado com sucesso!"

@pytest.mark.asyncio
async def test_integration_image_message(mock_waha_api_server, waha_receiver_server, mock_process_message_logic, monkeypatch):
    chat_id = "user_image@c.us"
    image_url = "http://localhost:3000/media/image_test.jpg"
    image_message_payload = {
        "event": "message",
        "chatId": chat_id,
        "type": "image",
        "mediaUrl": image_url
    }

    # Mock do _ocr_image para simular o OCR
    mock_ocr = MagicMock(return_value="Texto extraído da imagem.")
    monkeypatch.setattr("resipaia.py_waha_receiver.WahaReceiver._ocr_image", mock_ocr)

    mock_process_message_logic.return_value = {"to": chat_id, "message": "Imagem processada com sucesso!"}

    response = send_webhook_request(image_message_payload)
    assert response == {"status": "received"}

    await asyncio.sleep(1) # Aguarda o processamento em background

    mock_ocr.assert_called_once_with(image_url)
    mock_process_message_logic.assert_called_once()
    called_args = mock_process_message_logic.call_args[0][0]
    assert called_args["body"] == "Texto extraído da imagem."

    response_data = requests.get("http://127.0.0.1:8001/_get_responses").json()
    assert len(response_data["responses"]) == 1
    assert response_data["responses"][0]["chatId"] == chat_id
    assert response_data["responses"][0]["text"] == "Imagem processada com sucesso!"
