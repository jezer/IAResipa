# Databricks notebook source
!pip install /dbfs/FileStore/mcp-server/mcp-server-databricks-0.1.0.whl

# COMMAND ----------
from mcp_server import MCPServer
from pyspark.sql import SparkSession

# COMMAND ----------
# Configurar Spark Session
spark = SparkSession.builder.appName("MCPServer").getOrCreate()

# COMMAND ----------
# Inicializar MCP Server
server = MCPServer()

# COMMAND ----------
# Exemplo de uso com PySpark
def process_with_mcp(content: str):
    request = {
        "content": content,
        "source": "databricks",
        "context": {"spark_context": True}
    }
    return server.handle_request(request)

# Registrar como UDF
spark.udf.register("mcp_process", process_with_mcp)

# COMMAND ----------
# Exemplo de uso com DataFrame
df = spark.createDataFrame([
    ("Analise este código Python",),
    ("Revise a qualidade deste módulo",)
], ["request"])

result_df = df.selectExpr("request", "mcp_process(request) as mcp_response")
