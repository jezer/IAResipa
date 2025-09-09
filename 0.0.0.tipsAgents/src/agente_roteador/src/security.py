from datetime import datetime, timedelta
from typing import Optional, Dict
import jwt
from cryptography.fernet import Fernet
import hashlib
import logging
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
import time

logger = logging.getLogger(__name__)

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests = {}

    def check_rate_limit(self, client_id: str) -> bool:
        now = time.time()
        minute_ago = now - 60

        # Limpar requisições antigas
        self.requests[client_id] = [
            req_time for req_time in self.requests.get(client_id, [])
            if req_time > minute_ago
        ]

        # Verificar limite
        if len(self.requests.get(client_id, [])) >= self.requests_per_minute:
            return False

        # Adicionar nova requisição
        if client_id not in self.requests:
            self.requests[client_id] = []
        self.requests[client_id].append(now)
        return True


class SecurityLayer:
    def __init__(self, secret_key: str, token_expiration_minutes: int = 60):
        self.secret_key = secret_key
        self.cipher_suite = Fernet(Fernet.generate_key())
        self.token_expiration = token_expiration_minutes
        self.rate_limiter = RateLimiter()
        self.api_key_header = APIKeyHeader(name="X-API-Key")

    def encrypt_sensitive_data(self, data: str) -> str:
        """Encripta dados sensíveis"""
        return self.cipher_suite.encrypt(data.encode()).decode()

    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Decripta dados sensíveis"""
        return self.cipher_suite.decrypt(encrypted_data.encode()).decode()

    def generate_token(self, client_id: str, metadata: Optional[Dict] = None) -> str:
        """Gera um token JWT"""
        expiration = datetime.utcnow() + timedelta(minutes=self.token_expiration)
        payload = {
            "sub": client_id,
            "exp": expiration,
            "iat": datetime.utcnow(),
            "metadata": metadata or {}
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def validate_token(self, token: str) -> Dict:
        """Valida um token JWT"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            if datetime.fromtimestamp(payload["exp"]) < datetime.utcnow():
                raise HTTPException(status_code=401, detail="Token expirado")
            return payload
        except jwt.InvalidTokenError as e:
            logger.error(f"Token inválido: {str(e)}")
            raise HTTPException(status_code=401, detail="Token inválido")

    def check_rate_limit(self, client_id: str) -> bool:
        """Verifica o rate limit para um cliente"""
        if not self.rate_limiter.check_rate_limit(client_id):
            logger.warning(f"Rate limit excedido para cliente {client_id}")
            raise HTTPException(status_code=429, detail="Rate limit excedido")
        return True

    def hash_password(self, password: str) -> str:
        """Gera um hash seguro para senhas"""
        return hashlib.argon2.hash(password)

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verifica se uma senha corresponde ao hash"""
        return hashlib.argon2.verify(password, hashed)

    async def get_api_key(self, api_key: str = Security(APIKeyHeader(name="X-API-Key"))) -> str:
        """Valida a API key"""
        if not self.validate_api_key(api_key):
            raise HTTPException(
                status_code=401,
                detail="API key inválida"
            )
        return api_key

    def validate_api_key(self, api_key: str) -> bool:
        """Valida uma API key"""
        # Implementar lógica de validação da API key
        # Por exemplo, verificar contra um banco de dados ou lista de keys válidas
        return True  # Placeholder
