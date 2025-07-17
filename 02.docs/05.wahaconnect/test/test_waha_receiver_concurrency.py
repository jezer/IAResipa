import pytest
import requests
import threading
import time
import uvicorn
import asyncio
from fastapi import FastAPI, Request
from typing import Dict, List

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

# --- Testes de Concorrência para WahaReceiver ---

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
    # Importar o WahaReceiver aqui para evitar problemas de importação circular
    # e garantir que as variáveis de ambiente sejam carregadas corretamente.
    # Para este teste, vamos simular o ambiente.
    import os
    os.environ["WAHA_API_URL"] = "http://127.0.0.1:8001"
    os.environ["APP_HOST"] = "127.0.0.1"
    os.environ["APP_PORT"] = "8000"

    from resipaia.codbackup.py_waha_receiver import WahaReceiver

    receiver = WahaReceiver()
    
    # Rodar o servidor em uma thread separada
    server_thread = threading.Thread(target=receiver.start_server, daemon=True)
    server_thread.start()
    time.sleep(2) # Give the server a moment to start
    yield
    # No teardown needed as it's a daemon thread

@pytest.fixture(autouse=True)
def clear_mock_responses():
    # Limpa as respostas do mock antes de cada teste
    requests.get("http://127.0.0.1:8001/_clear_responses")
    yield

def send_webhook_request(chat_id: str):
    url = "http://127.0.0.1:8000/webhook"
    payload = {
        "event": "message",
        "chatId": chat_id,
        "body": f"Mensagem de teste de {chat_id}",
        "fromMe": False
    }
    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar requisição para {chat_id}: {e}")
        return None

@pytest.mark.asyncio
async def test_concurrency_with_multiple_messages(mock_waha_api_server, waha_receiver_server):
    num_messages = 10
    chat_ids = [f"user_{i}@c.us" for i in range(num_messages)]

    threads = []
    for chat_id in chat_ids:
        thread = threading.Thread(target=send_webhook_request, args=(chat_id,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Aguardar um pouco para que as tarefas assíncronas do receiver sejam concluídas
    await asyncio.sleep(2)

    # Verificar as respostas recebidas pelo mock da API do Waha
    response_data = requests.get("http://127.0.0.1:8001/_get_responses").json()
    actual_responses = response_data["responses"]

    assert len(actual_responses) == num_messages, f"Esperado {num_messages} respostas, mas recebeu {len(actual_responses)}"

    received_chat_ids = {resp["chatId"] for resp in actual_responses}
    expected_message = "Obrigado, iremos analisar."

    for chat_id in chat_ids:
        assert chat_id in received_chat_ids, f"ChatId {chat_id} não recebeu resposta."
        # Verificar se a resposta para este chat_id é a esperada
        # Como as respostas podem vir em qualquer ordem, precisamos encontrar a correta
        found_response = False
        for resp in actual_responses:
            if resp["chatId"] == chat_id and resp["text"] == expected_message:
                found_response = True
                break
        assert found_response, f"Resposta incorreta ou ausente para {chat_id}"

    print(f"Teste de concorrência concluído. Recebeu {len(actual_responses)} respostas esperadas.")
