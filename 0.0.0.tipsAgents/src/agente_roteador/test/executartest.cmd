@echo off
echo Mudando para o diretorio raiz do projeto (agente_roteador)...
cd ..

echo.
echo Executando os testes com pytest via Poetry...

poetry run pytest test/test_server.py -v

poetry run pytest test/test_commands_integration.py -v

echo.
echo Testes finalizados.
pause