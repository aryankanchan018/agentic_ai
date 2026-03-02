import asyncio
import json
import time
from typing import Dict, Any
import websockets

class MCPClient:
    """MCP Client for agent communication"""
    
    def __init__(self, agent_name: str, server_url: str = "ws://localhost:8765"):
        self.agent_name = agent_name
        self.server_url = server_url
        self.websocket = None
        self.message_handlers = {}
    
    async def connect(self):
        """Connect to MCP server"""
        self.websocket = await websockets.connect(self.server_url)
        
        # Register agent
        register_msg = {
            "method": "register",
            "params": {"agent_name": self.agent_name}
        }
        await self.websocket.send(json.dumps(register_msg))
        response = await self.websocket.recv()
        print(f"{self.agent_name} connected: {response}")
    
    async def send_message(self, receiver: str, method: str, params: Dict[str, Any]):
        """Send message to another agent via MCP"""
        message = {
            "id": f"{self.agent_name}_{int(time.time() * 1000)}",
            "method": method,
            "params": params,
            "sender": self.agent_name,
            "receiver": receiver,
            "timestamp": time.time()
        }
        
        await self.websocket.send(json.dumps(message))
        response = await self.websocket.recv()
        return json.loads(response)
    
    async def listen(self):
        """Listen for incoming messages"""
        async for message in self.websocket:
            data = json.loads(message)
            method = data.get('method')
            
            if method in self.message_handlers:
                handler = self.message_handlers[method]
                await handler(data)
    
    def register_handler(self, method: str, handler):
        """Register message handler"""
        self.message_handlers[method] = handler
    
    async def close(self):
        """Close connection"""
        if self.websocket:
            await self.websocket.close()
