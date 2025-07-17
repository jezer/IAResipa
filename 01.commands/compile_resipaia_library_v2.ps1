# compile_resipaia_library_v2.ps1

# Este script compila a biblioteca Python resipaia usando o módulo 'build',
# que é a ferramenta recomendada pela PyPA para criar pacotes de distribuição.

# Define o diretório raiz do projeto
$projectRoot = "C:\source\IAResipa\03.src" # Define o caminho para o diretório da biblioteca

# Navega para o diretório raiz do projeto
Set-Location $projectRoot

Write-Host "Verificando e instalando o módulo 'build' se necessário..."
# Verifica se o módulo 'build' está instalado e o instala se não estiver
try {
    python -m build --version | Out-Null
} catch {
    Write-Host "Módulo 'build' não encontrado. Instalando..."
    pip install build
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Erro ao instalar o módulo 'build'." -ForegroundColor Red
        exit 1
    }
}

# Limpa quaisquer builds anteriores
Write-Host "Limpando builds anteriores..."
Remove-Item -Path "dist", "build", "*.egg-info" -Recurse -ErrorAction SilentlyContinue

# Executa a compilação da biblioteca usando 'python -m build'
Write-Host "Iniciando a compilação da biblioteca com 'python -m build'..."
python -m build --sdist --wheel

if ($LASTEXITCODE -ne 0) {
    Write-Host "Erro na compilação da biblioteca. Verifique o log acima." -ForegroundColor Red
    exit 1
}

# Encontra o arquivo .whl gerado
$generatedWheelPath = Join-Path -Path "dist" -ChildPath "resipaia*.whl"
$wheelFile = Get-Item -Path $generatedWheelPath | Select-Object -ExpandProperty FullName

if (-not $wheelFile) {
    Write-Host "Erro: Arquivo .whl não encontrado após a compilação." -ForegroundColor Red
    exit 1
}

# Renomeia o arquivo .whl para incluir a data e hora e a versão do setup.py
$setupPyPath = Join-Path $projectRoot "setup.py"
$setupPyContent = Get-Content $setupPyPath | Out-String

# Extrai a versão usando uma regex
$versionMatch = [regex]::Match($setupPyContent, "version='([0-9.]+)'")
if ($versionMatch.Success) {
    $version = $versionMatch.Groups[1].Value
} else {
    Write-Host "Erro: No foi possvel encontrar a verso no setup.py." -ForegroundColor Red
    exit 1
}

$timestamp = Get-Date -Format "yyyy_MM_dd_HH_mm"
# $newWheelFileName = "resipaia_${version}_${timestamp}.whl"
$newWheelFileName = "resipaia-${version}-py3-none-any.whl"
$newWheelPath = Join-Path -Path "dist" -ChildPath $newWheelFileName

# Move e renomeia o arquivo
Move-Item -Path $wheelFile -Destination $newWheelPath -Force

Write-Host "Compilação concluída com sucesso! Pacote gerado: $newWheelPath" -ForegroundColor Green

# Opcional: Instalar a biblioteca localmente para teste
# Write-Host "Instalando a biblioteca localmente para teste..."
# pip install "$newWheelPath" --force-reinstall

# if ($LASTEXITCODE -ne 0) {
#     Write-Host "Erro na instalação local da biblioteca." -ForegroundColor Red
#     exit 1
# }

# Write-Host "Instalação local concluída." -ForegroundColor Green
