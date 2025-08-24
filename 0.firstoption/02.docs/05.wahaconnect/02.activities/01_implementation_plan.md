
# Plano de Atividades: Implementação do Conector Waha (Revisado)

## Etapa 1: Webhook Básico e Teste de Resposta Direta

O foco desta etapa é criar um webhook funcional que recebe uma mensagem e envia uma resposta fixa, garantindo que a comunicação básica com o Waha e os testes de concorrência funcionem.

-   [x] **Atividade 1.1: Estrutura e Configuração do `py_waha_receiver.py`**
    -   **Descrição:** Criar o arquivo `py_waha_receiver.py` em `03.src/resipaia/`. Implementar a classe `WahaReceiver` e um servidor web (FastAPI). A configuração (`waha_api_url`, `host`, `port`) deve ser carregada a partir de variáveis de ambiente (arquivo `.env`), não fixada no código.
    -   **Entradas:** `03.class_implementation_details.md`.
    -   **Saídas:** Arquivo `py_waha_receiver.py` com estrutura do servidor e gerenciamento de configuração.

-   [x] **Atividade 1.2: Implementar Resposta Fixa Assíncrona**
    -   **Descrição:** Implementar a rota `/webhook` para que responda imediatamente com `{"status": "received"}` e inicie o processamento da resposta em uma tarefa de fundo (background task). A tarefa de fundo deve chamar a lógica que envia a resposta fixa ("Obrigado, iremos analisar.") para o `chatId` correto.
    -   **Entradas:** `03.class_implementation_details.md`.
    -   **Saídas:** Webhook funcional que responde de forma assíncrona com uma mensagem padrão.

-   [x] **Atividade 1.3: Criar Teste de Concorrência Robusto**
    -   **Descrição:** Desenvolver o teste de concorrência. O teste deve simular múltiplos usuários enviando mensagens e verificar no `mock_waha_api` se cada um recebeu a resposta correta. O estado do mock (logs de chamadas) deve ser zerado a cada execução de teste para garantir o isolamento.
    -   **Entradas:** Documentos na pasta `test/`.
    -   **Saídas:** Testes `pytest` que validam a robustez do webhook contra condições de corrida.

## Etapa 2: Integração com o Processador Principal (`py_main_processor.py`) e Pré-processamento de Mídia

O foco desta etapa é integrar o webhook com a lógica de negócio existente e adicionar a capacidade de pré-processar mensagens de áudio e imagem para texto.

-   [x] **Atividade 2.1: Refatorar `py_main_processor.py` para ser Importável**
    -   **Descrição:** Modificar `py_main_processor.py` movendo a lógica de negócio para uma nova função com uma assinatura clara: `def process_message_logic(message_details: dict) -> dict:`. A função `main` e o bloco `if __name__ == "__main__":` serão adaptados para decodificar o JSON de `sys.argv` e chamar esta nova função, mantendo a compatibilidade existente.
    -   **Entradas:** `03.src/resipaia/py_main_processor.py`.
    -   **Saídas:** `py_main_processor.py` refatorado com uma função de lógica de negócio pura e importável.

-   [x] **Atividade 2.2: Implementar Transcrição de Áudio**
    -   **Descrição:** Implementar o método `_transcribe_audio` em `py_waha_receiver.py`. Esta atividade envolve a escolha de uma biblioteca/API de transcrição (ex: `SpeechRecognition` com `Whisper` ou uma API de nuvem), o download do arquivo de áudio e a conversão para texto.
    -   **Entradas:** `03.class_implementation_details.md`.
    -   **Saídas:** Método `_transcribe_audio` funcional e testado.

-   [x] **Atividade 2.3: Implementar OCR de Imagem**
    -   **Descrição:** Implementar o método `_ocr_image` em `py_waha_receiver.py`. Esta atividade envolve a escolha de uma biblioteca/API de OCR (ex: `Pillow` com `Tesseract` ou uma API de nuvem), o download da imagem e a extração de texto.
    -   **Entradas:** `03.class_implementation_details.md`.
    -   **Saídas:** Método `_ocr_image` funcional e testado.

-   [x] **Atividade 2.4: Atualizar Lógica de Pré-processamento em `process_message_from_waha`**
    -   **Descrição:** Modificar o método `process_message_from_waha` para identificar o tipo de mensagem (texto, áudio, imagem). Se for áudio, chamar `_transcribe_audio`; se for imagem, chamar `_ocr_image`. O texto resultante (ou o texto original da mensagem) será então usado para a próxima etapa.
    -   **Entradas:** `02.message_reception_flow.mmd`, `03.class_implementation_details.md`.
    -   **Saídas:** Lógica de pré-processamento de mídia implementada.

-   [x] **Atividade 2.5: Integrar `py_waha_receiver.py` com o Processador via Adaptador**
    -   **Descrição:** Criar uma função adaptadora separada (ex: `adapt_waha_to_processor_format`) para converter o payload do Waha (agora com o texto pré-processado) para o dicionário esperado por `process_message_logic`. O método principal (`process_message_from_waha`) irá chamar este adaptador e, em seguida, invocar a função `process_message_logic` do processador.
    -   **Entradas:** `py_waha_receiver.py`, `py_main_processor.py` refatorado.
    -   **Saídas:** O `WahaReceiver` delega a lógica de negócio para o processador através de um adaptador testável.

-   [x] **Atividade 2.6: Criar Testes de Integração de Ponta a Ponta (com Mídia)**
    -   **Descrição:** Criar um novo arquivo de teste (`test_waha_integration.py`). O teste irá simular chamadas ao endpoint `/webhook` com diferentes tipos de mensagens (texto, áudio, imagem). Usará o `mock_waha_api` para confirmar que a resposta final correta é enviada para o Waha e `pytest.monkeypatch` para espiar a chamada à função `process_message_logic` e garantir que o texto pré-processado correto foi passado.
    -   **Entradas:** `py_waha_receiver.py`, `py_main_processor.py`.
    -   **Saídas:** Testes de integração que garantem que o roteamento, pré-processamento e transformação de dados estão funcionando de ponta a ponta.
