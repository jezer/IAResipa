import subprocess
import datetime
import os

def run_and_log_tests():
    timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    log_dir = os.path.join("tests", "log")
    log_file_name = f"test_results_{timestamp}.md"
    log_file_path = os.path.join(log_dir, log_file_name)

    # Garante que o diretório de log exista
    os.makedirs(log_dir, exist_ok=True)

    print(f"Executando testes e salvando o log em: {log_file_path}")

    try:
        # Executa o pytest e captura a saída
        result = subprocess.run(
            ["pytest"],
            capture_output=True,
            text=True, # Para capturar stdout/stderr como texto
            check=False # Não levanta exceção para códigos de saída diferentes de 0
        )

        # Escreve a saída completa no arquivo de log
        with open(log_file_path, "w", encoding="utf-8") as f:
            f.write("# Resultados dos Testes - ")
            f.write(timestamp)
            f.write("\n\n```\n")
            f.write(result.stdout)
            f.write(result.stderr)
            f.write("\n```\n")
        
        if result.returncode == 0:
            print("Todos os testes passaram com sucesso!")
        else:
            print(f"Alguns testes falharam. Verifique o log em {log_file_path}")

    except FileNotFoundError:
        print("Erro: 'pytest' não encontrado. Certifique-se de que está instalado e no PATH.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao executar os testes: {e}")

if __name__ == "__main__":
    run_and_log_tests()
