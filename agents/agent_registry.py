"""Agent Registry for service discovery and management"""
from typing import Dict, List, Any
from datetime import datetime

class AgentRegistry:
    """Central registry for agent discovery and health monitoring"""
    
    def __init__(self):
        self.agents: Dict[str, Dict[str, Any]] = {}
        self.message_log: List[Dict[str, Any]] = []
    
    def register_agent(self, agent_name: str, capabilities: List[str], metadata: Dict = None):
        """Register an agent with its capabilities"""
        self.agents[agent_name] = {
            'name': agent_name,
            'capabilities': capabilities,
            'status': 'active',
            'registered_at': datetime.utcnow().isoformat(),
            'metadata': metadata or {},
            'message_count': 0
        }
        print(f"[Registry] Agent registered: {agent_name} with capabilities: {capabilities}")
    
    def unregister_agent(self, agent_name: str):
        """Unregister an agent"""
        if agent_name in self.agents:
            self.agents[agent_name]['status'] = 'inactive'
            print(f"[Registry] Agent unregistered: {agent_name}")
    
    def find_agent_by_capability(self, capability: str) -> List[str]:
        """Find agents that have a specific capability"""
        return [
            name for name, info in self.agents.items()
            if capability in info['capabilities'] and info['status'] == 'active'
        ]
    
    def get_agent_info(self, agent_name: str) -> Dict[str, Any]:
        """Get information about a specific agent"""
        return self.agents.get(agent_name, {})
    
    def log_message(self, sender: str, receiver: str, method: str, status: str, data: Any = None):
        """Log A2A communication"""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'sender': sender,
            'receiver': receiver,
            'method': method,
            'status': status,
            'data': data
        }
        self.message_log.append(log_entry)
        
        # Update message counts
        if sender in self.agents:
            self.agents[sender]['message_count'] += 1
    
    def get_message_log(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent message log"""
        return self.message_log[-limit:]
    
    def get_all_agents(self) -> Dict[str, Dict[str, Any]]:
        """Get all registered agents"""
        return self.agents
    
    def get_active_agents(self) -> List[str]:
        """Get list of active agent names"""
        return [name for name, info in self.agents.items() if info['status'] == 'active']
