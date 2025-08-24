# configure_environment.ps1

# Este script ajuda a configurar o ambiente de desenvolvimento para o projeto IAResipa.

Write-Host "--- Configuração do Ambiente IAResipa ---"

# 1. Configurar Variáveis de Ambiente do Supabase
Write-Host "`n1. Configurando Variáveis de Ambiente do Supabase"
Write-Host "Estas variáveis são necessárias para que seus scripts Python se conectem ao Supabase."
Write-Host "Elas serão definidas para a sessão atual do PowerShell."
Write-Host "Para torná-las persistentes, você pode usar 'setx' (requer privilégios de administrador) ou adicioná-las manualmente às Variáveis de Ambiente do Sistema."

$supabaseUrl = "https://cquaryyrqlypmzfajbho.supabase.co"
$supabaseKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNxdWFyeXlycWx5cG16ZmFqYmhvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE4MzY3NzcsImV4cCI6MjA2NzQxMjc3N30.rd-CWbup_U-9DYFbmpGXaxlbyEOcBoTaIM6SMUAu5gk"

# Define para a sessão atual
$env:SUPABASE_URL = $supabaseUrl
$env:SUPABASE_KEY = $supabaseKey
Write-Host "   Supabase URL e Key definidos para a sessão atual." -ForegroundColor Green

# 2. Comandos Docker
Write-Host "`n2. Comandos Docker"
Write-Host "Certifique-se de que o Docker Desktop esteja em execução."

$PSScriptRoot = "C:\source\IAResipa"
# Caminho para o docker-compose.yml
$projectRoot = Split-Path -Path $PSScriptRoot -Parent
$dockerComposeDir = Join-Path $projectRoot "04.deploy" "docker"
$dockerComposePath = Join-Path $dockerComposeDir "docker-compose.yml"

if (Test-Path $dockerComposePath) {
    Write-Host "`n   Arquivo Docker Compose encontrado em: $dockerComposePath" -ForegroundColor Green
    Write-Host "   Para gerenciar seus serviços Docker, navegue até este diretório e execute os comandos:
"
    Write-Host "   cd ""$dockerComposeDir"""
    Write-Host "   docker-compose up -d --build   (Para construir e iniciar os serviços)"
    Write-Host "   docker-compose down           (Para parar e remover os serviços)"
} else {
    Write-Host "`n   Aviso: docker-compose.yml não encontrado no caminho esperado: $dockerComposePath" -ForegroundColor Yellow
    Write-Host "   Por favor, certifique-se de que seu arquivo Docker Compose esteja corretamente posicionado."
}

# 3. Compilação da Biblioteca Python (resipaia)
Write-Host "`n3. Compilação da Biblioteca Python (resipaia)"
Write-Host "   Para compilar a biblioteca Python 'resipaia' (gera o arquivo .whl em dist/):"
Write-Host "   powershell.exe -ExecutionPolicy Bypass -File ""$PSScriptRoot\compile_resipaia_library_v2.ps1""" -ForegroundColor Cyan

# 4. Configuração do Ambiente Python (Máquina Host - Opcional)
Write-Host "`n4. Configuração do Ambiente Python (Máquina Host - Opcional)"
Write-Host "   Se você planeja executar scripts Python ou testes diretamente em sua máquina host (fora do Docker):"
Write-Host "   - Certifique-se de que Python e pip estejam instalados."
Write-Host "   - Instale as dependências do projeto (se houver requirements.txt na raiz do projeto):"
Write-Host "     pip install -r requirements.txt" -ForegroundColor Cyan
Write-Host "   - Execute os testes (salva o log em tests/log/):"
Write-Host "     powershell.exe -ExecutionPolicy Bypass -File ""$PSScriptRoot\run_and_log_tests.py""" -ForegroundColor Cyan

Write-Host "`n--- Guia de Configuração Concluído ---"
Write-Host "Lembre-se de reiniciar seu terminal para que as variáveis de ambiente persistentes (se definidas) entrem em vigor."
