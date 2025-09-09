import logging
from typing import Dict, Any, List
from datetime import datetime
import google.generativeai as genai
from .models import Analysis, MCPResponse, MCPRequest, RoutingDecision

class BaseAdapter:
    async def format_response(self, response: MCPResponse) -> Dict:
        raise NotImplementedError

class GeminiAdapter(BaseAdapter):
    async def format_response(self, response: MCPResponse) -> Dict:
        return {
            "response": response.content,
            "metadata": {
                **response.metadata,
                "format": "gemini_structured"
            }
        }

class ClaudeAdapter(BaseAdapter):
    async def format_response(self, response: MCPResponse) -> Dict:
        return {
            "completion": response.content,
            "metadata": response.metadata,
            "stop_reason": "completed"
        }

class CopilotAdapter(BaseAdapter):
    async def format_response(self, response: MCPResponse) -> Dict:
        return {
            "suggestions": [response.content],
            "metadata": response.metadata
        }

class CursorAdapter(BaseAdapter):
    async def format_response(self, response: MCPResponse) -> Dict:
        return {
            "completion": response.content,
            "metadata": response.metadata
        }
