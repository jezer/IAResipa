import sys
import json
import os
import io

# Se a biblioteca 'resipaia' estiver instalada (via .whl no Docker, por exemplo),
# ela pode ser importada diretamente como um pacote Python.
# Não há necessidade de manipular sys.path para importações de pacotes instalados.
from resipaia.py_main_processor import main as py_main_processor_main

def main():
    # --- SIMULAÇÃO DO AMBIENTE N8N (items[0].json) ---
    # No ambiente real do n8n, 'items' seria uma variável global
    # contendo a entrada do nó anterior. Aqui, criamos um exemplo
    # para simular essa entrada, que é o JSON completo que o Waha
    # enviaria para o n8n.
    simulated_n8n_input = {
        "messages": [
            {
                "session": "mock_session_123",
                "PushName": "MockUser",
                "Chat": "mock_chat_id_abc",
                "id": "mock_msg_id_xyz",
                "event": "message",
                "fromMe": False,
                "text": {"body": "Olá, quero reservar um quiosque."},
                "body": "Olá, quero reservar um quiosque.",
                "from": "5511999998888"
            }
        ]
    }

    # No n8n, você acessaria os dados assim:
    # message_data = items[0].json
    # Para simular isso, usamos o 'simulated_n8n_input' diretamente.
    # O py_main_processor espera o JSON completo do Waha como uma string.
    waha_message_body_for_processor = json.dumps(simulated_n8n_input)

    # --- CHAMADA À FUNÇÃO PRINCIPAL DA BIBLIOTECA RESIPAIA ---
    # Salva o stdout original e sys.argv original
    original_stdout = sys.stdout
    original_argv = sys.argv

    # Redireciona stdout para capturar a saída do py_main_processor
    captured_output = io.StringIO()
    sys.stdout = captured_output

    try:
        # Simula o ambiente sys.argv que py_main_processor.main espera.
        # O primeiro elemento de sys.argv é o nome do script que está sendo executado.
        # O segundo elemento é o JSON stringificado da mensagem do Waha.
        sys.argv = ["py_main_processor.py", waha_message_body_for_processor]
        
        # Chama a função main da biblioteca resipaia
        py_main_processor_main()

        # Obtém a saída capturada
        response_from_processor = captured_output.getvalue()
        
        # Imprime a saída do py_main_processor de volta para o stdout (para o n8n)
        original_stdout.write(response_from_processor)

    except Exception as e:
        # Em caso de erro, imprime uma mensagem de erro formatada para o n8n
        error_response = {"to": "error", "message": f"Erro ao processar a mensagem no Python: {e}"}
        original_stdout.write(json.dumps(error_response))
    finally:
        # Restaura o stdout e sys.argv originais
        sys.stdout = original_stdout
        sys.argv = original_argv

if __name__ == "__main__":
    main()
