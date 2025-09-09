@echo off
echo === Criando wheel do MCP Server ===

cd C:\source\IAResipa\0.0.0.tipsAgents\src\agente_roteador\compile\databricks

REM Limpar builds anteriores
echo 2. Limpando builds anteriores...
if exist "dist" rd /s /q "dist"
if exist "build" rd /s /q "build"
if exist "mcp_server_databricks.egg-info" rd /s /q "mcp_server_databricks.egg-info"

REM Construir o pacote wheel
echo 3. Construindo wheel package...
cd ..\..\
python -m build --wheel
cd compile\databricks

echo.
echo === Build Completo ===
echo O arquivo .whl está disponível em: dist/mcp_server_databricks-0.1.0-py3-none-any.whl
echo.

REM Opcionalmente instalar o wheel localmente para teste
set /p INSTALL_LOCAL=Deseja instalar o wheel localmente para teste? (S/N): 
if /i "%INSTALL_LOCAL%"=="S" (
    pip install --force-reinstall dist/mcp_server_databricks-0.1.0-py3-none-any.whl
    echo Wheel instalado localmente com sucesso!
)

pause
