#!/bin/bash

# Define o diretório raiz do projeto dentro do contêiner
PROJECT_ROOT="/usr/src/app" # Ajuste conforme o caminho onde seu projeto está no Docker

# Navega para o diretório raiz do projeto
cd "$PROJECT_ROOT"

# Instala as dependências do projeto (se houver um requirements.txt)
# pip install -r requirements.txt

# Compila a biblioteca resipaia
python -m build --sdist --wheel

# Encontra o arquivo .whl gerado (assumindo que está em dist/)
RESIPAIA_WHL=$(find dist -name "resipaia-*.whl" | head -n 1)

if [ -z "$RESIPAIA_WHL" ]; then
    echo "Erro: Arquivo .whl da resipaia não encontrado."
    exit 1
fi

# Instala a biblioteca resipaia
pip install "$RESIPAIA_WHL"

echo "Biblioteca resipaia instalada com sucesso!"

# Opcional: Limpar arquivos de build
# rm -rf dist build *.egg-info
