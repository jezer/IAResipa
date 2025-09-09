#!/bin/bash

# Configurar ambiente
python -m pip install --upgrade pip wheel setuptools build
python -m pip install databricks-connect

# Construir o pacote wheel
python -m build --wheel

# Criar diretório no DBFS
databricks fs mkdirs dbfs:/FileStore/mcp-server/

# Fazer upload do wheel para o DBFS
databricks fs cp dist/mcp_server_databricks-0.1.0-py3-none-any.whl dbfs:/FileStore/mcp-server/

# Instalar no cluster (substitua CLUSTER_ID pelo seu ID de cluster)
databricks clusters libraries install --cluster-id $CLUSTER_ID --whl dbfs:/FileStore/mcp-server/mcp_server_databricks-0.1.0-py3-none-any.whl
