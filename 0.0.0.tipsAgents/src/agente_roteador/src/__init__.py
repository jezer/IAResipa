"""
MCP Server - Model Context Protocol Server
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .server import MCPServer
from .models import MCPRequest, MCPResponse, Analysis
from .router import Router

__all__ = ["MCPServer", "MCPRequest", "MCPResponse", "Analysis", "Router"]

# Empty file to mark directory as Python package
