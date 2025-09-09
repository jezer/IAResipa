@echo off
REM Script para build e deploy no Databricks

REM Configurar ambiente
pip install --upgrade pip wheel setuptools build databricks-connect

REM Construir o pacote wheel
cd ..\..\
python -m build --wheel
cd compile\databricks

REM Configurar Databricks CLI (necessário ter configurado antes)
REM databricks configure --token

REM Criar diretório no DBFS
databricks fs mkdirs dbfs:/FileStore/mcp-server/

REM Upload do wheel para DBFS
databricks fs cp dist/mcp_server_databricks-0.1.0-py3-none-any.whl dbfs:/FileStore/mcp-server/

REM Nota: Substitua CLUSTER_ID pelo seu ID de cluster
set CLUSTER_ID=your-cluster-id-here
databricks clusters libraries install --cluster-id %CLUSTER_ID% --whl dbfs:/FileStore/mcp-server/mcp_server_databricks-0.1.0-py3-none-any.whl

echo Deployment completo! Verifique o status no console Databricks.
