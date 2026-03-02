import asyncio
import json
from typing import Dict, Any, List
from dataclasses import dataclass, asdict
import websockets

@dataclass
class MCPMessage:
    """Model Context Protocol message structure"""
    id: str
    method: str
    params: Dict[str, Any]
    sender: str
    receiver: str
    timestamp: float

class MCPServer:
    """MCP Server for agent communication"""
    
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.connections = {}
        self.message_queue = []
    
    async def register_agent(self, websocket, agent_name: str):
        """Register an agent connection"""
        self.connections[agent_name] = websocket
        print(f"Agent registered: {agent_name}")
    
    async def handle_message(self, websocket, message: str):
        """Handle incoming MCP messages"""
        try:
            data = json.loads(message)
            mcp_msg = MCPMessage(**data)
            
            # Route message to receiver
            if mcp_msg.receiver in self.connections:
                receiver_ws = self.connections[mcp_msg.receiver]
                await receiver_ws.send(json.dumps(asdict(mcp_msg)))
            else:
                # Queue message if receiver not connected
                self.message_queue.append(mcp_msg)
            
            return {"status": "delivered", "message_id": mcp_msg.id}
        
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    async def handler(self, websocket, path):
        """WebSocket connection handler"""
        agent_name = None
        
        try:
            async for message in websocket:
                data = json.loads(message)
                
                if data.get('method') == 'register':
                    agent_name = data.get('params', {}).get('agent_name')
                    await self.register_agent(websocket, agent_name)
                    await websocket.send(json.dumps({"status": "registered"}))
                
                else:
                    result = await self.handle_message(websocket, message)
                    await websocket.send(json.dumps(result))
        
        except websockets.exceptions.ConnectionClosed:
            if agent_name and agent_name in self.connections:
                del self.connections[agent_name]
                print(f"Agent disconnected: {agent_name}")
    
    async def start(self):
        """Start MCP server"""
        async with websockets.serve(self.handler, self.host, self.port):
            print(f"MCP Server running on ws://{self.host}:{self.port}")
            await asyncio.Future()  # Run forever

if __name__ == "__main__":
    server = MCPServer()
    asyncio.run(server.start())
