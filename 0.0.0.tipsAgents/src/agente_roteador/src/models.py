from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class SubTask(BaseModel):
    id: str
    parent_request_id: str
    intent: str
    domains: List[str]
    content: str
    target_client_id: Optional[str]
    dependencies: List[str] = []
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class SubTaskResult(BaseModel):
    subtask_id: str
    content: str
    metadata: Dict[str, Any]
    status: TaskStatus
    error: Optional[str]
    completed_at: datetime = Field(default_factory=datetime.utcnow)


class Analysis(BaseModel):
    intent: str
    domains: List[str]
    confidence: float
    requires_decomposition: bool = False
    suggested_subtasks: List[Dict[str, Any]] = []
    metadata: Dict[str, Any] = {}


class RoutingDecision(BaseModel):
    request_id: str
    rules_used: List[str]
    confidence: float
    result: str
    selected_clients: List[str]
    metadata: Dict[str, Any] = {}

    def is_valid(self) -> bool:
        return self.result == "valid" and len(self.selected_clients) > 0


class MCPRequest(BaseModel):
    content: str
    source: str
    context: Dict[str, Any] = {}
    headers: Dict[str, Any] = {}
    metadata: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)


class MCPResponse(BaseModel):
    success: bool
    content: Any
    metadata: Dict[str, Any] = {}
    error: Optional[str] = None
    completed_at: datetime = Field(default_factory=datetime.utcnow)


class CacheEntry(BaseModel):
    key: str
    value: Any
    expires_at: datetime
    metadata: Dict[str, Any] = {}


class MetricsData(BaseModel):
    request_count: int = 0
    error_count: int = 0
    avg_response_time: float = 0.0
    cache_hits: int = 0
    cache_misses: int = 0
    last_updated: datetime = Field(default_factory=datetime.utcnow)
