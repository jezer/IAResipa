# Script para simular uma solicitação de usuário para criar um agente de plano de testes
$env:PYTHONPATH = "C:\source\IAResipa"

# Ativa o ambiente Python (ajuste o caminho conforme necessário)
$pythonPath = "C:\Program Files\Python313\python.exe"

# Solicita a criação do agente via agente_roteador
$pythonScript = @"
import asyncio
import sys
sys.path.append('C:\\source\\IAResipa\\0.0.0.tipsAgents\\0.0.Global\\0.0.agente_roteador')
from agente_roteador import route_request

async def main():
    prompt = '''
    Preciso de um agente que gere planos de teste detalhados para nossos sistemas. 
    O agente deve ser capaz de criar cenários Gherkin, planos de teste em tabela, 
    casos de teste passo a passo, e scripts de setup/teardown. 
    É importante que os testes sigam boas práticas como dados determinísticos, 
    critérios de aceite claros e nomenclatura rastreável.
    '''
    
    result = await route_request(prompt)
    print("\nResposta do Agente Roteador:")
    print("-----------------------------")
    print(json.dumps(result, indent=2, ensure_ascii=False))

asyncio.run(main())
"@

# Salva o script Python temporário
$tempScript = New-TemporaryFile
[System.IO.File]::WriteAllText($tempScript.FullName, $pythonScript)

# Executa o script Python
& $pythonPath $tempScript.FullName

# Remove o arquivo temporário
Remove-Item $tempScript.FullName
