# run_tests.ps1

# Este script executa o script Python run_and_log_tests.py,
# que por sua vez executa os testes Pytest e salva os resultados em um arquivo de log.

# Define o caminho para o script Python
$pythonScriptPath = Join-Path $PSScriptRoot "run_and_log_tests.py"

Write-Host "Executando testes e registrando os resultados..."

# Executa o script Python
python "$pythonScriptPath"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Ocorreu um erro durante a execução dos testes. Verifique o log." -ForegroundColor Red
    exit 1
}

Write-Host "Execução dos testes concluída. Verifique a pasta tests/log/ para os resultados." -ForegroundColor Green
