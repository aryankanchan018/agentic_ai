"""Enhanced MCP Server with agent registry integration"""
import asyncio
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
import websockets
from datetime import datetime

@dataclass
class MCPMessage:
    """Model Context Protocol message structure"""
    id: str
    method: str
    params: Dict[str, Any]
    sender: str
    receiver: str
    timestamp: float

class EnhancedMCPServer:
    """Enhanced MCP Server for agent communication with registry"""
    
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.connections: Dict[str, Any] = {}
        self.message_queue: List[MCPMessage] = []
        self.agent_registry: Dict[str, Dict[str, Any]] = {}
        self.message_log: List[Dict[str, Any]] = []
    
    async def register_agent(self, websocket, agent_name: str, capabilities: List[str] = None):
        """Register an agent connection"""
        self.connections[agent_name] = websocket
        self.agent_registry[agent_name] = {
            'name': agent_name,
            'capabilities': capabilities or [],
            'status': 'active',
            'connected_at': datetime.utcnow().isoformat(),
            'message_count': 0
        }
        print(f"[MCP Server] Agent registered: {agent_name}")
        
        # Send registration confirmation
        await websocket.send(json.dumps({
            'status': 'registered',
            'agent_name': agent_name,
            'server_time': datetime.utcnow().isoformat()
        }))
    
    async def handle_message(self, websocket, message: str) -> Dict[str, Any]:
        """Handle incoming MCP messages"""
        try:
            data = json.loads(message)
            mcp_msg = MCPMessage(**data)
            
            # Log message
            self.message_log.append({
                'timestamp': datetime.utcnow().isoformat(),
                'sender': mcp_msg.sender,
                'receiver': mcp_msg.receiver,
                'method': mcp_msg.method,
                'message_id': mcp_msg.id
            })
            
            # Update sender message count
            if mcp_msg.sender in self.agent_registry:
                self.agent_registry[mcp_msg.sender]['message_count'] += 1
            
            # Route message to receiver
            if mcp_msg.receiver in self.connections:
                receiver_ws = self.connections[mcp_msg.receiver]
                await receiver_ws.send(json.dumps(asdict(mcp_msg)))
                return {'status': 'delivered', 'message_id': mcp_msg.id}
            else:
                # Queue message if receiver not connected
                self.message_queue.append(mcp_msg)
                return {'status': 'queued', 'message_id': mcp_msg.id, 'reason': 'receiver_offline'}
        
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    async def handle_discovery(self, capability: str) -> Dict[str, Any]:
        """Handle agent discovery by capability"""
        matching_agents = [
            name for name, info in self.agent_registry.items()
            if capability in info.get('capabilities', []) and info['status'] == 'active'
        ]
        return {
            'status': 'success',
            'capability': capability,
            'agents': matching_agents
        }
    
    async def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all registered agents"""
        return {
            'status': 'success',
            'total_agents': len(self.agent_registry),
            'active_agents': len([a for a in self.agent_registry.values() if a['status'] == 'active']),
            'agents': self.agent_registry,
            'total_messages': len(self.message_log)
        }
    
    async def handler(self, websocket, path):
        """WebSocket connection handler"""
        agent_name = None
        
        try:
            async for message in websocket:
                data = json.loads(message)
                method = data.get('method')
                
                if method == 'register':
                    agent_name = data.get('params', {}).get('agent_name')
                    capabilities = data.get('params', {}).get('capabilities', [])
                    await self.register_agent(websocket, agent_name, capabilities)
                
                elif method == 'discover':
                    capability = data.get('params', {}).get('capability')
                    result = await self.handle_discovery(capability)
                    await websocket.send(json.dumps(result))
                
                elif method == 'get_status':
                    result = await self.get_agent_status()
                    await websocket.send(json.dumps(result))
                
                else:
                    result = await self.handle_message(websocket, message)
                    await websocket.send(json.dumps(result))
        
        except websockets.exceptions.ConnectionClosed:
            if agent_name:
                if agent_name in self.connections:
                    del self.connections[agent_name]
                if agent_name in self.agent_registry:
                    self.agent_registry[agent_name]['status'] = 'disconnected'
                print(f"[MCP Server] Agent disconnected: {agent_name}")
    
    async def start(self):
        """Start MCP server"""
        async with websockets.serve(self.handler, self.host, self.port):
            print(f"[MCP Server] Running on ws://{self.host}:{self.port}")
            await asyncio.Future()

if __name__ == "__main__":
    server = EnhancedMCPServer()
    asyncio.run(server.start())
