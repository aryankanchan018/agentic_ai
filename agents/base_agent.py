"""Base Agent class with MCP integration for A2A communication"""
import asyncio
import json
from typing import Dict, Any, Callable, Optional
from abc import ABC, abstractmethod
import sys
sys.path.append('..')
from mcp_server.client import MCPClient

class BaseAgent(ABC):
    """Base class for all agents with MCP support"""
    
    def __init__(self, agent_name: str, mcp_enabled: bool = True):
        self.agent_name = agent_name
        self.mcp_enabled = mcp_enabled
        self.mcp_client: Optional[MCPClient] = None
        self.capabilities = []
        self.message_handlers = {}
        
    async def initialize(self):
        """Initialize agent and connect to MCP server"""
        if self.mcp_enabled:
            self.mcp_client = MCPClient(self.agent_name)
            try:
                await self.mcp_client.connect()
                self._register_handlers()
            except Exception as e:
                print(f"[{self.agent_name}] MCP connection failed: {e}. Running in standalone mode.")
                self.mcp_enabled = False
    
    def _register_handlers(self):
        """Register message handlers with MCP client"""
        if self.mcp_client:
            for method, handler in self.message_handlers.items():
                self.mcp_client.register_handler(method, handler)
    
    async def send_message(self, receiver: str, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send A2A message via MCP"""
        if self.mcp_enabled and self.mcp_client and self.mcp_client.connected:
            await self.mcp_client.send_message(receiver, method, params)
            return {"status": "sent", "receiver": receiver, "method": method}
        else:
            # Fallback to direct call
            return {"status": "direct_call", "warning": "MCP not available"}
    
    @abstractmethod
    def get_capabilities(self) -> list:
        """Return list of agent capabilities"""
        pass
    
    @abstractmethod
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming request"""
        pass
    
    async def shutdown(self):
        """Cleanup and disconnect"""
        if self.mcp_client:
            await self.mcp_client.disconnect()
