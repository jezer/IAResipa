from supabase import create_client, Client
import time
import uuid

# Configuração (substitua pelos seus valores)
SUPABASE_URL = "https://cquaryyrqlypmzfajbho.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNxdWFyeXlycWx5cG16ZmFqYmhvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE4MzY3NzcsImV4cCI6MjA2NzQxMjc3N30.rd-CWbup_U-9DYFbmpGXaxlbyEOcBoTaIM6SMUAu5gk"
TEST_EMAIL = f"jezer.portilho@gmail.com"
TEST_PASSWORD = "Arthur*01"
TEST_TABLE = "recursos"  # Usando a tabela 'recursos' para testes de CRUD

def test_conexao_autenticacao():
    """Testa conexão básica e autenticação"""
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # 1. Teste de conexão básica
        inicio = time.time()
        health = supabase.auth.get_session()
        latency = (time.time() - inicio) * 1000
        print(f"✅ Conexão básica OK | Latência: {latency:.2f}ms")
        
        # 2. Cadastro de usuário teste
        user = supabase.auth.sign_up({
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        })
        
        if not user.user:
            raise Exception("Falha no cadastro")
        
        print(f"✅ Autenticação OK | User ID: {user.user.id}")
        return supabase, user
        
    except Exception as e:
        print(f"❌ Falha na conexão/autenticação: {str(e)}")
        return None, None

def test_conexao_autenticacao2():
    """Teste de conexão e criação de usuário temporário"""
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Teste de conexão
        inicio = time.time()
        supabase.auth.get_session()
        print(f"✅ Conexão OK | Latência: {(time.time()-inicio)*1000:.2f}ms")
        
        # Cria usuário teste
        email = TEST_EMAIL
        user = supabase.auth.sign_up({
            "email": email,
            "password": TEST_PASSWORD
        })
        print(f"✅ Autenticação OK | User: {email}")
        return supabase
        
    except Exception as e:
        print(f"❌ Falha na conexão: {str(e)}")
        return None

def test_crud(supabase: Client):
    """Teste CRUD em tabela existente"""
    try:
        # Dados de teste
        test_data = {
            "name": f"Recurso Teste {uuid.uuid4().hex[:4]}",
            "capacity": 10
        }
        
        # INSERT
        insert = supabase.table(TEST_TABLE).insert(test_data).execute()
        item_id = insert.data[0]['id']
        print(f"✅ INSERT OK | ID: {item_id}")
        
        # SELECT
        item = supabase.table(TEST_TABLE)\
                     .select("*")\
                     .eq("id", item_id)\
                     .single()\
                     .execute()
        print(f"✅ SELECT OK | Nome: {item.data['name']}")
        
        # UPDATE
        supabase.table(TEST_TABLE)\
              .update({"capacity": 20})\
              .eq("id", item_id)\
              .execute()
        print("✅ UPDATE OK")
        
        # DELETE
        supabase.table(TEST_TABLE)\
              .delete()\
              .eq("id", item_id)\
              .execute()
        print("✅ DELETE OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Falha no CRUD: {str(e)}")
        return False

def test_crud_tabela(supabase: Client):
    """Teste completo de CRUD"""
    try:
        # Usando uma tabela existente ou criando via SQL (com permissões)
        table_name = "recursos"  # Usando a tabela 'recursos' para testes de CRUD
        
        # 1. Inserção
        test_data = {"name": "Item Teste", "capacity": 42}
        insert_response = supabase.table(table_name).insert(test_data).execute()
        inserted_id = insert_response.data[0]['id']
        
        # 2. Leitura
        select_response = supabase.table(table_name)\
                               .select("*")\
                               .eq("id", inserted_id)\
                               .execute()
        
        # 3. Atualização
        update_response = supabase.table(table_name)\
                                .update({"capacity": 99})\
                                .eq("id", inserted_id)\
                                .execute()
        
        # 4. Deleção
        delete_response = supabase.table(table_name)\
                                .delete()\
                                .eq("id", inserted_id)\
                                .execute()
        
        print("✅ CRUD completo OK")
        return True
        
    except Exception as e:
        print(f"❌ Falha no CRUD: {str(e)}")
        return False

def test_consulta_publica(supabase: Client):
    """Teste de consulta em tabela existente"""
    try:
        # Substitua por uma tabela REAL do seu projeto
        public_table = "cadastro_pessoas_fisica"  # Usando a tabela 'cadastro_pessoas_fisica'
        
        response = supabase.table(public_table)\
                         .select("*", count='exact')\
                         .limit(1)\
                         .execute()
        
        print(f"✅ Consulta pública OK | Total registros: {response.count}")
        return True
        
    except Exception as e:
        print(f"❌ Falha na consulta pública: {str(e)}")
        return False

# if __name__ == "__main__":
#     print("🚀 Iniciando testes Supabase")
    
#     # Etapa 1: Conexão e Autenticação
#     supabase, user = test_conexao_autenticacao()
    
#     if supabase:
#         # Etapa 2: Testes com tabelas
#         print("\n🔧 Testando CRUD...")
#         crud_ok = test_crud_tabela(supabase)
        
#         print("\n🔍 Testando consulta pública...")
#         consulta_ok = test_consulta_publica(supabase)
    
#     print("\n📊 Resultado Final:")
#     if supabase and crud_ok and consulta_ok:
#         print("✅ TODOS OS TESTES PASSARAM!")
#     else:
#         print("⚠️ Alguns testes falharam. Verifique os logs acima.")
    
#     # Não tenta deletar usuário (precisa de service role key)
#     print("\n🧹 Obs: Usuário teste não foi removido (requer permissões admin)")

if __name__ == "__main__":
    print("🚀 Teste Supabase - Versão Simplificada")
    sb = test_conexao_autenticacao2()
    if sb:
        # 2. Teste CRUD
        print("\n🔧 Testando CRUD básico...")
        if test_crud(sb):
            print("\n🎉 Todos os testes passaram!")
        else:
            print("\n⚠️ CRUD falhou - Verifique:")
            print(f"- A tabela '{TEST_TABLE}' existe?")
            print("- Permissões RLS estão configuradas?")
            print("- Estrutura da tabela tem campos 'name' e 'capacity'?"
)



