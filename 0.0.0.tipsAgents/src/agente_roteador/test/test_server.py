from src.models import MCPRequest
from src.server import MCPServer, app
import asyncio
import json
import yaml
import pytest
from pathlib import Path
from fastapi.testclient import TestClient

@pytest.fixture
def config_path(tmp_path):
    """Create temporary config directory with test files."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    
    # Define test configurations
    test_configs = {
        "sources.yaml": """
            capabilities: "capabilities.yaml"
            routing_rules: "routing_rules.yaml"
            gemini_prompts: "prompts.md"
            gemini_api_key: "AIzaSyBbR52zZ37OlDXtNjWS_Nq85QXXG7E_hMw"
            openai_api_key: "TEST_OPENAI_KEY_123"
        """.strip(),
        "capabilities.yaml": """
            clients:
              default_client:
                type: "openai"
                capabilities: ["text_generation", "code_generation"]
                confidence_threshold: 0.5
        """.strip(),
        "routing_rules.yaml": """
            default_rules:
              min_confidence: 0.5
              fallback_client: "default_client"
        """.strip(),
        "prompts.md": """
            # Test Prompts
            ## Default
            Test prompt template
        """.strip()
    }
    
    # Create all test config files
    for filename, content in test_configs.items():
        (config_dir / filename).write_text(content)
    
    return config_dir

@pytest.fixture
def mock_genai(monkeypatch):
    """Mock Google GenerativeAI for testing."""
    class MockGenerativeModel:
        def __init__(self, model_name, api_key, generation_config):
            self.model_name = model_name
            self.api_key = api_key
            self.config = generation_config
        
        async def generate_content(self, *args, **kwargs):
            class MockResponse:
                def text(self):
                    return "Mock response"
            return MockResponse()

    class MockGenAI:
        GenerativeModel = MockGenerativeModel

    monkeypatch.setattr("google.generativeai", MockGenAI)
    return MockGenAI

@pytest.mark.asyncio
async def test_request(config_path, mock_genai, monkeypatch):
    """Test server request handling with test config."""
    # Ensure config directory exists
    config_path.mkdir(parents=True, exist_ok=True)
    
    # Create test configuration files
    config_files = {
        "sources.yaml": {
            "default_client": {
                "type": "openai",
                "config": {
                    "api_key": "dummy_key",
                    "model": "gpt-4"
                }
            },
            "fallback_client": {
                "type": "anthropic",
                "config": {
                    "api_key": "dummy_key",
                    "model": "claude-2"
                }
            },
            "gemini_api_key": "TEST_GEMINI_KEY_123",
            "capabilities": "capabilities.yaml",
            "routing_rules": "routing_rules.yaml",
            "gemini_prompts": "prompts.md"
        },
        "capabilities.yaml": {
            "clients": {
                "test_client": {
                    "capabilities": ["test"]
                }
            }
        },
        "routing_rules.yaml": {
            "rules": []
        }
    }
    
    # Write all config files
    for filename, content in config_files.items():
        with open(config_path / filename, "w") as f:
            yaml.dump(content, f)
    
    # Create empty prompts file
    (config_path / "prompts.md").write_text("# Test Prompts")
    
    # Patch config directory path
    monkeypatch.setattr("src.server.Path", lambda x: config_path)
    
    # Debug output
    print(f"\nTest config path: {config_path}")
    print("\nActual sources.yaml content:")
    print((config_path / "sources.yaml").read_text())
    
    server = MCPServer()
    client = TestClient(app)
    
    response = client.post("/analyze", json={
        "content": "Test message",
        "source": "test",
        "context": {}
    }, headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
