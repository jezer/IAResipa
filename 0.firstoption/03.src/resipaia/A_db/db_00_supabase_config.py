import os
from supabase import create_client, Client
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from dotenv import load_dotenv
load_dotenv()

def get_supabase_client() -> Client:
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")
    # As credenciais devem ser carregadas de variáveis de ambiente para produção.
    # Para testes locais, você pode usar um arquivo .env e carregar com `dotenv`.
    # Exemplo:
    # from dotenv import load_dotenv
    # load_dotenv()
    # supabase_url = os.environ.get("SUPABASE_URL")
    # supabase_key = os.environ.get("SUPABASE_KEY")
    #
    # Para fins de teste e desenvolvimento, se as variáveis de ambiente não estiverem definidas,
    # você pode usar valores padrão (NÃO RECOMENDADO PARA PRODUÇÃO):
    # if not supabase_url:
    #     supabase_url = "SUA_URL_SUPABASE_AQUI"
    # if not supabase_key:
    #     supabase_key = "SUA_CHAVE_SUPABASE_AQUI"

    if not supabase_url or not supabase_key:
        logging.error("Variáveis de ambiente SUPABASE_URL ou SUPABASE_KEY não configuradas.")
        raise ValueError("Credenciais do Supabase não configuradas.")
    try:
        client: Client = create_client(supabase_url, supabase_key)
        logging.info("Cliente Supabase criado com sucesso.")
        return client
    except Exception as e:
        logging.error(f"Erro ao criar cliente Supabase: {e}")
        raise

if __name__ == "__main__":
    # Exemplo de uso (apenas para teste)
    try:
        supabase_client = get_supabase_client()
        # Você pode adicionar um teste simples aqui, como:
        # response = supabase_client.from_("your_table").select("*").execute()
        # print(response.data)
    except ValueError as e:
        print(f"Erro de configuração: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")
