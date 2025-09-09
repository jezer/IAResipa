from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime

class AgentType(Enum):
    GLOBAL = "global"
    SPECIFIC = "specific"

class ActionType(Enum):
    ROUTE = "route"
    SPLIT = "split_and_route"
    REJECT = "reject"

class CommunicationType(Enum):
    SYNC = "synchronous"
    ASYNC = "asynchronous"

@dataclass
class AgentConfig:
    id: str
    priority: int
    capability: str
    type: AgentType

@dataclass
class CommunicationConfig:
    type: CommunicationType
    timeout: int
    retry: int
    input_path: Optional[str] = None
    output_path: Optional[str] = None
    format: Optional[str] = None

@dataclass
class LogConfig:
    level: str
    format: Dict[str, str]
    retention: str
    rotation: str
    path: str

@dataclass
class RouterConfig:
    available_agents: List[AgentConfig]
    policies: Dict[str, List[str]]
    logging: LogConfig
    communication: Dict[str, CommunicationConfig]

@dataclass
class Task:
    sequence: int
    target_agent: str
    priority: int
    content: str
    reasoning: Dict[str, Any]
    depends_on: Optional[List[str]] = None

@dataclass
class RoutingDecision:
    request_id: str
    timestamp: datetime
    action: ActionType
    tasks: List[Task]
    reason: Optional[Dict[str, str]] = None
    suggestion: Optional[Dict[str, str]] = None

    def to_dict(self) -> Dict:
        return {
            "request_id": self.request_id,
            "timestamp": self.timestamp.isoformat(),
            "action": self.action.value,
            "tasks": [
                {
                    "sequence": task.sequence,
                    "target_agent": task.target_agent,
                    "priority": task.priority,
                    "content": task.content,
                    "reasoning": task.reasoning,
                    "depends_on": task.depends_on
                }
                for task in self.tasks
            ],
            "reason": self.reason,
            "suggestion": self.suggestion
        }
