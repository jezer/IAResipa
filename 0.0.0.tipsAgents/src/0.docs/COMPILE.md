# Instruções para Compilação do MCP Server

## 1. Preparação do Ambiente

```bash
# 1. Instalar ferramentas de compilação
pip install pyinstaller
pip install -e .

# 2. Configurar variáveis de ambiente para compilação otimizada
set PYTHONOPTIMIZE=2
set PYTHONHASHSEED=1
set PYTHONDONTWRITEBYTECODE=1
```

## 2. Processo de Compilação

```bash
# Compilar usando PyInstaller com o arquivo spec
pyinstaller mcp-server.spec --clean

# O executável será gerado em ./dist/mcp-server
```

## 3. Estrutura do Pacote Compilado

Após a compilação, você terá:

```
dist/
└── mcp-server/
    ├── mcp-server.exe      # Executável principal
    ├── config/             # Arquivos de configuração
    │   ├── capabilities.yaml
    │   ├── routing_rules.md
    │   ├── prompts.md
    │   └── schemas/
    └── .env                # Configurações de ambiente
```

## 4. Verificações Pós-Compilação

1. Testar o executável:
```bash
./dist/mcp-server/mcp-server.exe
```

2. Verificar logs:
```bash
tail -f ./dist/mcp-server/logs/mcp-server.log
```

## 5. Notas Importantes

1. **Otimizações**: 
   - PYTHONOPTIMIZE=2 remove docstrings e assertions
   - Bytecode é otimizado para máxima performance

2. **Segurança**:
   - Arquivos sensíveis como .env precisam ser protegidos
   - Chaves API devem ser gerenciadas separadamente

3. **Distribuição**:
   - O executável é standalone (inclui Python runtime)
   - Todas as dependências estão empacotadas
   - Config pode ser modificada sem recompilar

4. **Performance**:
   - Código compilado é geralmente mais rápido
   - Uso de memória pode ser maior
   - Startup inicial pode ser mais lento

## 6. Troubleshooting

1. **Erro de DLL não encontrada**:
   - Verifique se todas as dependências estão instaladas
   - Use `depends.exe` para verificar DLLs faltantes

2. **Erro de módulo não encontrado**:
   - Adicione o módulo em `hiddenimports` no .spec
   - Verifique se o módulo está instalado

3. **Erro de arquivo de configuração**:
   - Verifique se todos os arquivos estão em `datas` no .spec
   - Confirme os caminhos relativos
