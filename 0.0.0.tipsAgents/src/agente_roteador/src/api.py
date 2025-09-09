from fastapi import FastAPI, HTTPException
from .server import MCPServer
from .models import MCPRequest, MCPResponse

app = FastAPI(title="MCP Router API")
server = MCPServer()

@app.post("/analyze")
async def analyze_request(request: MCPRequest) -> MCPResponse:
    """
    Endpoint para análise de solicitações
    """
    try:
        return await server.handle_request(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/capabilities")
async def get_capabilities():
    """
    Endpoint para listar capacidades disponíveis
    """
    return server.config["capabilities"]
