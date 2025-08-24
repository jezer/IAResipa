def solicitar_ao_gemini(instrucoes_path, prompt_usuario):
    try:
        with open(instrucoes_path, 'r', encoding='utf-8') as f:
            instrucoes = f.read()

        prompt_completo = f"Siga estas instruções:\n\n{instrucoes}\n\nAgora, {prompt_usuario}"

        # Aqui você faria a chamada real ao Gemini CLI ou à API do Gemini
        # Por exemplo, se você tiver uma função que interage com o Gemini CLI:
        # resultado = gemini_cli_interface.send_prompt(prompt_completo)
        # print(resultado)
        print(f"Prompt enviado ao Gemini:\n{prompt_completo}") # Para demonstração

    except FileNotFoundError:
        print(f"Erro: Arquivo de instruções não encontrado em '{instrucoes_path}'")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Exemplo de uso:
# Digamos que você quer gerar código Python:
instrucao_python_path = "./instrucoes_gemini/codigo_python/instrucoes_python.md"
meu_pedido = "crie uma função Python que calcula o fatorial de um número."
solicitar_ao_gemini(instrucao_python_path, meu_pedido)

# Ou para gerenciar pastas:
instrucao_pastas_path = "./instrucoes_gemini/pastas/instrucoes_pastas.md"
meu_pedido_pastas = "organize os arquivos de log na pasta 'logs' por data."
solicitar_ao_gemini(instrucao_pastas_path, meu_pedido_pastas)

import google.generativeai as genai
import os
import time
import concurrent.futures

# Configure a chave da API (substitua pela sua chave real ou use variáveis de ambiente)
# genai.configure(api_key="SUA_API_KEY") 
# É melhor carregar a chave de uma variável de ambiente por segurança:
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def send_prompt_to_gemini(prompt: str, model_name: str = "gemini-pro", temperature: float = 0.7, max_output_tokens: int = 1024) -> str:
    """
    Envia um prompt para o modelo Gemini e retorna a resposta.
    Esta função não pergunta nada ao usuário.
    """
    try:
        model = genai.GenerativeModel(model_name=model_name)
        # Use o método generate_content que é síncrono e não interativo
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_output_tokens,
            )
        )
        # Retorna o texto da resposta, ou uma string vazia se não houver texto
        return response.text if response.candidates else ""
    except Exception as e:
        print(f"Erro ao chamar a API do Gemini: {e}")
        return f"ERRO: {e}"

# Exemplo de uso:
# response_text = send_prompt_to_gemini("Me dê uma breve introdução sobre computação quântica.")
# print(response_text)


import google.generativeai as genai
import os
import time
import concurrent.futures

# Configure a chave da API (substitua pela sua chave real ou use variáveis de ambiente)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def _send_prompt_internal(prompt: str, model_name: str, temperature: float, max_output_tokens: int) -> str:
    """
    Função interna que faz a chamada real à API do Gemini.
    """
    try:
        model = genai.GenerativeModel(model_name=model_name)
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_output_tokens,
            )
        )
        return response.text if response.candidates else ""
    except Exception as e:
        # Captura exceções da API e as retorna como parte do erro
        raise RuntimeError(f"Erro interno da API Gemini: {e}")

def send_prompt_with_timeout(prompt: str, timeout_seconds: int = 60, model_name: str = "gemini-pro", temperature: float = 0.7, max_output_tokens: int = 1024) -> str:
    """
    Envia um prompt para o modelo Gemini com um tempo limite.
    Não pergunta nada ao usuário.
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(_send_prompt_internal, prompt, model_name, temperature, max_output_tokens)
        try:
            return future.result(timeout=timeout_seconds)
        except concurrent.futures.TimeoutError:
            print(f"Tempo limite de {timeout_seconds} segundos excedido para o prompt.")
            return "ERRO: Tempo limite excedido."
        except RuntimeError as e:
            # Captura erros propagados da função interna
            print(f"Erro durante a execução da chamada Gemini: {e}")
            return f"ERRO: {e}"
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
            return f"ERRO: {e}"

# --- Exemplos de Uso ---

# Exemplo 1: Chamada bem-sucedida (tempo limite de 30 segundos)
print("--- Teste 1: Chamada bem-sucedida ---")
response_1 = send_prompt_with_timeout("Qual a capital da França?", timeout_seconds=30)
print(f"Resposta 1: {response_1}")
print("-" * 30)

# Exemplo 2: Simulação de Timeout (defina um timeout muito baixo para ver o erro)
print("--- Teste 2: Simulação de Timeout ---")
# Para realmente testar o timeout, a resposta do Gemini precisaria demorar.
# Aqui, simulamos um timeout baixo para um prompt simples, que provavelmente será rápido.
# Em um cenário real, você testaria com prompts mais complexos que exigem mais processamento.
response_2 = send_prompt_with_timeout("Descreva o ciclo da água em detalhes.", timeout_seconds=1) # Timeout propositalmente baixo
print(f"Resposta 2: {response_2}")
print("-" * 30)

# Exemplo 3: Usando suas instruções (você carregaria o conteúdo do arquivo aqui)
# Suponha que 'instrucoes_python_content' seja o texto do seu arquivo instrucoes_python.md
instrucoes_python_content = """
# Instruções para Geração de Código Python
Siga estas diretrizes ao criar ou modificar código Python:
## 1. Clareza e Legibilidade
* **Comentários:** Adicione comentários explicativos.
* **Nomenclatura:** Use nomes descritivos e em snake_case.
"""
complex_prompt = f"{instrucoes_python_content}\n\nAgora, crie uma função Python para calcular a sequência de Fibonacci."
print("--- Teste 3: Chamada com Instruções ---")
response_3 = send_prompt_with_timeout(complex_prompt, timeout_seconds=45)
print(f"Resposta 3: {response_3[:200]}...") # Imprime apenas os primeiros 200 caracteres
print("-" * 30)