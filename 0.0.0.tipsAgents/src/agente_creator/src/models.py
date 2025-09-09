from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class AgentType(Enum):
    MCP_CLIENT = "mcpclient"
    MCP_SERVER = "mcpserver"


class AgentConfig(BaseModel):
    name: str
    type: AgentType
    description: str
    capabilities: List[str]
    dependencies: List[str] = []
    config: Dict[str, Any] = {}


class CreatorRequest(BaseModel):
    agent_type: AgentType
    name: str
    description: str
    capabilities: List[str]
    config: Dict[str, Any] = {}
    template_overrides: Optional[Dict[str, str]] = None
    metadata: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CreatorResponse(BaseModel):
    success: bool
    agent_path: Optional[str]
    config_files: List[str] = []
    error: Optional[str] = None
    metadata: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)


class TemplateData(BaseModel):
    agent_type: AgentType
    name: str
    description: str
    capabilities: List[str]
    dependencies: List[str]
    config: Dict[str, Any]
    metadata: Dict[str, Any]
