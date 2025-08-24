# Script PowerShell para iniciar o py_waha_receiver_v2.py
#
# Este script inicia o servidor FastAPI do py_waha_receiver.py.
# Certifique-se de que as variáveis de ambiente (WAHA_API_URL, APP_HOST, APP_PORT)
# estejam configuradas no seu arquivo .env na raiz do projeto, pois o script Python as carrega.
#
# Para parar o servidor, pressione Ctrl+C no terminal onde este script está sendo executado.

Write-Host "Iniciando py_waha_receiver_v2.py..."

# Navega para o diretório raiz do projeto para garantir que o .env seja carregado corretamente
Set-Location "C:\source\IAResipa"

# Executa o script Python
python .\03.src\resipaia\wahaconnect\py_waha_receiver_v2.py

Write-Host "Servidor py_waha_receiver_v2.py parado."

