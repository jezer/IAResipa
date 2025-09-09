import uvicorn
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

if __name__ == "__main__":
    uvicorn.run(
        "src.api:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
