# Databricks Deployment Guide

## 1. Preparação do Pacote

1. Estrutura do pacote para Databricks:
```
mcp-server-databricks/
├── src/
│   └── mcp_server/
│       ├── __init__.py
│       ├── server.py
│       ├── router.py
│       └── config/
│           ├── capabilities.yaml
│           ├── routing_rules.md
│           └── prompts.md
├── setup.py
└── pyproject.toml
```

## 2. Configuração do Ambiente Databricks

1. **Requisitos do Cluster**:
   - Runtime: Databricks Runtime 7.3 ML ou superior
   - Python: 3.8 ou superior
   - Permissões: DBFS write access

2. **Variáveis de Ambiente**:
   Configure no escopo do cluster:
   ```
   GEMINI_API_KEY=AIzaSyBbR52zZ37OlDXtNjWS_Nq85QXXG7E_hMw
   MCP_CONFIG_PATH=/dbfs/FileStore/mcp-server/config
   ```

## 3. Instalação

1. **Local Build e Upload**:
   ```bash
   # Execute o script de deploy
   ./deploy.sh
   ```

2. **Instalação no Cluster**:
   - Via UI: Adicione o wheel em Libraries
   - Via CLI: Use o comando no deploy.sh

## 4. Uso no Databricks

1. **Notebook Import**:
   - Importe example_notebook.py como notebook
   - Execute as células em ordem

2. **Uso em Produção**:
   ```python
   from mcp_server import MCPServer
   
   # Inicializar
   server = MCPServer()
   
   # Usar como UDF
   spark.udf.register("mcp_process", server.handle_request)
   ```

## 5. Integração com Workflows

1. **Job Configuration**:
   ```json
   {
     "name": "MCP Processing Job",
     "existing_cluster_id": "cluster-id",
     "notebook_task": {
       "notebook_path": "/path/to/your/notebook",
       "base_parameters": {
         "input_table": "default.requests",
         "output_table": "default.responses"
       }
     }
   }
   ```

## 6. Monitoramento

1. **Logs**:
   - Localização: `/dbfs/FileStore/mcp-server/logs`
   - Rotação: 7 dias

2. **Métricas**:
   - Ganglia metrics no cluster
   - Custom metrics via MLflow

## 7. Troubleshooting

1. **Problemas Comuns**:
   - Permissões DBFS
   - Dependências conflitantes
   - Timeouts em requests

2. **Verificações**:
   ```python
   # Test import
   from mcp_server import MCPServer
   
   # Test configuration
   server = MCPServer()
   print(server.config)
   ```

## 8. Best Practices

1. **Performance**:
   - Use broadcast variables para configs
   - Cache resultados frequentes
   - Configure particionamento adequado

2. **Segurança**:
   - Use Databricks secrets
   - Implemente rate limiting
   - Monitore uso de recursos
