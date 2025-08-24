#!/bin/bash

# Este script instala a biblioteca resipaia a partir de um arquivo .whl
# que já deve ter sido copiado para o diretório de trabalho do contêiner.

# Encontra o arquivo .whl (assumindo que está no diretório atual)
RESIPAIA_WHL=$(find . -maxdepth 1 -name "resipaia-*.whl" | head -n 1)

if [ -z "$RESIPAIA_WHL" ]; then
    echo "Erro: Arquivo .whl da resipaia não encontrado no diretório atual."
    exit 1
fi

# Instala a biblioteca resipaia
pip install "$RESIPAIA_WHL"

echo "Biblioteca resipaia instalada com sucesso!"

# Opcional: Limpar o arquivo .whl após a instalação
# rm "$RESIPAIA_WHL"
