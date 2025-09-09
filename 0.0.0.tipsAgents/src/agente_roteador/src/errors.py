from typing import Optional, Dict, Any
import logging
import traceback
from datetime import datetime

logger = logging.getLogger(__name__)

class MCPError(Exception):
    """Classe base para exceções do MCP"""
    def __init__(self, message: str, error_code: str, details: Optional[Dict] = None):
        super().__init__(message)
        self.error_code = error_code
        self.details = details or {}
        self.timestamp = datetime.utcnow()

class ValidationError(MCPError):
    """Erro de validação de dados"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, "VALIDATION_ERROR", details)

class RoutingError(MCPError):
    """Erro no processo de roteamento"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, "ROUTING_ERROR", details)

class SecurityError(MCPError):
    """Erro relacionado à segurança"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, "SECURITY_ERROR", details)

class LLMError(MCPError):
    """Erro na comunicação com LLM"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, "LLM_ERROR", details)

class ConfigurationError(MCPError):
    """Erro na configuração do sistema"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, "CONFIG_ERROR", details)

def handle_error(error: Exception) -> Dict[str, Any]:
    """Manipula e formata erros para resposta"""
    if isinstance(error, MCPError):
        error_response = {
            "success": False,
            "error": {
                "code": error.error_code,
                "message": str(error),
                "details": error.details,
                "timestamp": error.timestamp.isoformat()
            }
        }
    else:
        error_response = {
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Erro interno do servidor",
                "details": {
                    "error_type": error.__class__.__name__,
                    "error_message": str(error)
                },
                "timestamp": datetime.utcnow().isoformat()
            }
        }

    # Logging do erro
    logger.error(
        f"Error occurred: {error_response['error']['code']}",
        extra={
            "error_details": error_response["error"],
            "stack_trace": traceback.format_exc()
        }
    )

    return error_response

class ErrorHandler:
    """Classe para gerenciamento centralizado de erros"""
    
    @staticmethod
    def validate_request(request: Dict) -> None:
        """Valida uma requisição"""
        required_fields = ["content", "source"]
        missing_fields = [field for field in required_fields if field not in request]
        
        if missing_fields:
            raise ValidationError(
                f"Campos obrigatórios ausentes: {', '.join(missing_fields)}",
                {"missing_fields": missing_fields}
            )

    @staticmethod
    def validate_configuration(config: Dict) -> None:
        """Valida configuração do sistema"""
        required_configs = ["capabilities", "routing_rules"]
        missing_configs = [conf for conf in required_configs if conf not in config]
        
        if missing_configs:
            raise ConfigurationError(
                f"Configurações obrigatórias ausentes: {', '.join(missing_configs)}",
                {"missing_configs": missing_configs}
            )

    @staticmethod
    def check_security(token: str, required_permissions: list) -> None:
        """Verifica requisitos de segurança"""
        if not token:
            raise SecurityError(
                "Token de autenticação ausente",
                {"required_permissions": required_permissions}
            )

    @staticmethod
    def handle_llm_error(error: Exception, llm_source: str) -> None:
        """Trata erros específicos de LLM"""
        raise LLMError(
            f"Erro na comunicação com {llm_source}: {str(error)}",
            {
                "llm_source": llm_source,
                "original_error": str(error),
                "error_type": error.__class__.__name__
            }
        )
