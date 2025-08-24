import pytest
from unittest.mock import patch, MagicMock
import os
import sys

# Adiciona o diretório pai ao sys.path para permitir importações relativas


from resipaia import get_supabase_client

@pytest.fixture
def mock_env_vars():
    with patch.dict(os.environ, {
        "SUPABASE_URL": "http://mock-url.com",
        "SUPABASE_KEY": "mock-key"
    }):
        yield

def test_get_supabase_client_success(mock_env_vars):
    with patch('resipaia.A_db.db_00_supabase_config.create_client') as mock_create_client:
        mock_client = MagicMock()
        mock_create_client.return_value = mock_client
        
        client = get_supabase_client()
        
        mock_create_client.assert_called_once_with("http://mock-url.com", "mock-key")
        assert client == mock_client

def test_get_supabase_client_missing_url():
    with patch.dict(os.environ, {"SUPABASE_URL": "", "SUPABASE_KEY": "mock-key"}):
        with pytest.raises(ValueError, match="Credenciais do Supabase não configuradas."):
            get_supabase_client()

def test_get_supabase_client_missing_key():
    with patch.dict(os.environ, {"SUPABASE_URL": "http://mock-url.com", "SUPABASE_KEY": ""}):
        with pytest.raises(ValueError, match="Credenciais do Supabase não configuradas."):
            get_supabase_client()

def test_get_supabase_client_creation_error(mock_env_vars):
    with patch('resipaia.A_db.db_00_supabase_config.create_client') as mock_create_client:
        mock_create_client.side_effect = Exception("Erro de conexão")
        with pytest.raises(Exception, match="Erro de conexão"):
            get_supabase_client()
