from typing import Dict, Any, List
import asyncio
import time
from datetime import datetime
from .constraint_agent import ConstraintAgent
from .optimization_agent import OptimizationAgent
from .conflict_resolution_agent import ConflictResolutionAgent
from .resource_allocation_agent import ResourceAllocationAgent
from .validation_agent import ValidationAgent
from .monitoring_agent import MonitoringAgent
from .analytics_agent import AnalyticsAgent
from .agent_registry import AgentRegistry

class AgentOrchestrator:
    """Orchestrates multi-agent collaboration using A2A communication"""
    
    def __init__(self, mcp_enabled: bool = False):
        # Initialize agents
        self.validation_agent = ValidationAgent()
        self.resource_agent = ResourceAllocationAgent()
        self.optimization_agent = OptimizationAgent()
        self.constraint_agent = ConstraintAgent()
        self.conflict_agent = ConflictResolutionAgent()
        self.monitoring_agent = MonitoringAgent()
        self.analytics_agent = AnalyticsAgent()
        
        # Agent registry
        self.registry = AgentRegistry()
        self.mcp_enabled = mcp_enabled
        self.initialized = False
    
    async def initialize(self):
        """Initialize all agents and register them"""
        if self.initialized:
            return
        
        agents = [
            self.validation_agent,
            self.resource_agent,
            self.optimization_agent,
            self.constraint_agent,
            self.conflict_agent,
            self.monitoring_agent,
            self.analytics_agent
        ]
        
        # Initialize agents with MCP if enabled
        if self.mcp_enabled:
            for agent in agents:
                await agent.initialize()
        
        # Register agents
        for agent in agents:
            self.registry.register_agent(
                agent.agent_name,
                agent.get_capabilities(),
                {'mcp_enabled': self.mcp_enabled}
            )
        
        self.initialized = True
        print("[Orchestrator] All agents initialized and registered")
    
    async def send_agent_message(self, sender: str, receiver_agent, method: str, params: Dict) -> Dict:
        """Send message between agents with logging"""
        self.registry.log_message(sender, receiver_agent.agent_name, method, 'sent', params)
        
        # Use MCP if enabled, otherwise direct call
        if self.mcp_enabled and receiver_agent.mcp_enabled:
            await receiver_agent.send_message(receiver_agent.agent_name, method, params)
        
        # Process request directly
        result = await receiver_agent.process_request({'method': method, 'params': params})
        
        self.registry.log_message(receiver_agent.agent_name, sender, method, 'completed', result)
        return result
    
    def generate_timetable(self, input_data: Dict) -> Dict:
        """Main workflow: orchestrate agents to generate timetable (sync wrapper)"""
        # Run async workflow in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            if not self.initialized:
                loop.run_until_complete(self.initialize())
            result = loop.run_until_complete(self._generate_timetable_async(input_data))
            return result
        finally:
            loop.close()
    
    async def _generate_timetable_async(self, input_data: Dict) -> Dict:
        """Main async workflow: orchestrate agents to generate timetable"""
        start_time = time.time()
        
        # Track generation start
        await self.send_agent_message(
            "Orchestrator",
            self.monitoring_agent,
            "track_performance",
            {'event_type': 'generation_started', 'timestamp': datetime.utcnow().isoformat()}
        )
        
        # Step 1: Validation Agent validates input data
        print("[Orchestrator] Step 1: Validating input data...")
        validation_result = await self.send_agent_message(
            "Orchestrator",
            self.validation_agent,
            "validate_data",
            input_data
        )
        
        if validation_result['status'] == 'invalid':
            return {
                'status': 'failed',
                'reason': 'Invalid input data',
                'errors': validation_result['errors'],
                'message_log': self.registry.get_message_log()
            }
        
        # Step 2: Check data completeness
        print("[Orchestrator] Step 2: Checking data completeness...")
        completeness_result = await self.send_agent_message(
            "Orchestrator",
            self.validation_agent,
            "check_completeness",
            input_data
        )
        
        if completeness_result['status'] == 'incomplete':
            print(f"[Orchestrator] Warning: Missing fields: {completeness_result['missing_fields']}")
        
        # Step 3: Resource Allocation Agent allocates rooms
        print("[Orchestrator] Step 3: Allocating rooms...")
        room_allocation = await self.send_agent_message(
            "Orchestrator",
            self.resource_agent,
            "allocate_rooms",
            {
                'requirements': {'requests': input_data.get('requirements', [])},
                'rooms': input_data.get('rooms', [])
            }
        )
        
        # Step 4: Optimization Agent generates initial timetable
        print("[Orchestrator] Step 4: Generating optimal timetable...")
        optimization_result = await self.send_agent_message(
            "Orchestrator",
            self.optimization_agent,
            "optimize_timetable",
            input_data
        )
        
        if optimization_result['status'] == 'infeasible':
            generation_time = time.time() - start_time
            await self.send_agent_message(
                "Orchestrator",
                self.monitoring_agent,
                "track_performance",
                {
                    'event_type': 'generation_completed',
                    'status': 'failed',
                    'generation_time': generation_time
                }
            )
            return {
                'status': 'failed',
                'reason': 'No feasible timetable found',
                'message_log': self.registry.get_message_log()
            }
        
        timetable = optimization_result['assignments']
        
        # Step 5: Constraint Agent validates timetable
        print("[Orchestrator] Step 5: Validating constraints...")
        enriched_data = self._enrich_timetable_data(timetable, input_data)
        constraint_result = await self.send_agent_message(
            "Orchestrator",
            self.constraint_agent,
            "validate_constraints",
            enriched_data
        )
        
        constraints = constraint_result.get('constraints', [])
        violated = [c for c in constraints if c.get('violated', False)]
        
        # Step 6: If conflicts exist, Conflict Resolution Agent resolves them
        if violated:
            print(f"[Orchestrator] Step 6: Resolving {len(violated)} conflicts...")
            await self.send_agent_message(
                "Orchestrator",
                self.monitoring_agent,
                "track_performance",
                {'event_type': 'constraint_violation', 'count': len(violated)}
            )
            
            resolution = await self.send_agent_message(
                "Orchestrator",
                self.conflict_agent,
                "resolve_conflicts",
                {'timetable': timetable, 'constraints': constraints}
            )
        
        # Step 7: Calculate utilization metrics
        print("[Orchestrator] Step 7: Calculating utilization metrics...")
        utilization_result = await self.send_agent_message(
            "Orchestrator",
            self.optimization_agent,
            "calculate_utilization",
            {'timetable': timetable}
        )
        
        floor_optimization = await self.send_agent_message(
            "Orchestrator",
            self.resource_agent,
            "optimize_floor_allocation",
            {'allocations': timetable, 'rooms': input_data.get('rooms', [])}
        )
        
        # Step 8: Analytics Agent generates insights
        print("[Orchestrator] Step 8: Generating analytics insights...")
        analytics_result = await self.send_agent_message(
            "Orchestrator",
            self.analytics_agent,
            "analyze_timetable",
            {'timetable': timetable}
        )
        
        insights_result = await self.send_agent_message(
            "Orchestrator",
            self.analytics_agent,
            "generate_insights",
            {'timetable': timetable}
        )
        
        recommendations_result = await self.send_agent_message(
            "Orchestrator",
            self.analytics_agent,
            "recommend_improvements",
            {'timetable': timetable}
        )
        
        # Track completion
        generation_time = time.time() - start_time
        await self.send_agent_message(
            "Orchestrator",
            self.monitoring_agent,
            "track_performance",
            {
                'event_type': 'generation_completed',
                'status': 'success',
                'generation_time': generation_time
            }
        )
        
        print(f"[Orchestrator] Timetable generation completed in {generation_time:.2f}s")
        
        return {
            'status': 'success',
            'timetable': timetable,
            'constraints': constraints,
            'utilization': utilization_result.get('utilization', {}),
            'floor_optimization': floor_optimization,
            'analytics': analytics_result.get('statistics', {}),
            'insights': insights_result.get('insights', []),
            'recommendations': recommendations_result.get('recommendations', []),
            'generation_time': generation_time,
            'message_log': self.registry.get_message_log(),
            'agent_status': self.registry.get_all_agents()
        }
    
    def _enrich_timetable_data(self, timetable: List[Dict], input_data: Dict) -> Dict:
        """Enrich timetable with additional data for validation"""
        rooms = {r['id']: r for r in input_data.get('rooms', [])}
        subjects = {s['id']: s for s in input_data.get('subjects', [])}
        divisions = {d['id']: d for d in input_data.get('divisions', [])}
        
        enriched_entries = []
        for entry in timetable:
            room = rooms.get(entry['room_id'], {})
            subject = subjects.get(entry['subject_id'], {})
            division = divisions.get(entry['division_id'], {})
            
            enriched_entries.append({
                **entry,
                'room_capacity': room.get('capacity', 0),
                'room_is_lab': room.get('is_lab', False),
                'subject_is_lab': subject.get('is_lab', False),
                'student_count': division.get('student_count', 0)
            })
        
        return {'entries': enriched_entries}
