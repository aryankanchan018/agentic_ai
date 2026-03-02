from typing import Dict, Any, List
from .constraint_agent import ConstraintAgent
from .optimization_agent import OptimizationAgent
from .conflict_resolution_agent import ConflictResolutionAgent
from .resource_allocation_agent import ResourceAllocationAgent

class AgentOrchestrator:
    """Orchestrates multi-agent collaboration using A2A communication"""
    
    def __init__(self):
        self.constraint_agent = ConstraintAgent()
        self.optimization_agent = OptimizationAgent()
        self.conflict_agent = ConflictResolutionAgent()
        self.resource_agent = ResourceAllocationAgent()
        self.message_log = []
    
    def log_message(self, sender: str, receiver: str, message: str, data: Any = None):
        """Log A2A communication"""
        self.message_log.append({
            'sender': sender,
            'receiver': receiver,
            'message': message,
            'data': data
        })
    
    def generate_timetable(self, input_data: Dict) -> Dict:
        """Main workflow: orchestrate agents to generate timetable"""
        
        # Step 1: Resource Allocation Agent allocates rooms
        self.log_message("Orchestrator", "ResourceAllocationAgent", "Allocate rooms")
        room_allocation = self.resource_agent.allocate_rooms(
            {'requests': input_data.get('requirements', [])},
            input_data.get('rooms', [])
        )
        
        # Step 2: Optimization Agent generates initial timetable
        self.log_message("Orchestrator", "OptimizationAgent", "Generate optimal timetable")
        optimization_result = self.optimization_agent.optimize_timetable(input_data)
        
        if optimization_result['status'] == 'infeasible':
            return {
                'status': 'failed',
                'reason': 'No feasible timetable found',
                'message_log': self.message_log
            }
        
        timetable = optimization_result['assignments']
        
        # Step 3: Constraint Agent validates timetable
        self.log_message("Orchestrator", "ConstraintAgent", "Validate timetable")
        
        # Enrich timetable data for validation
        enriched_data = self._enrich_timetable_data(timetable, input_data)
        constraints = self.constraint_agent.validate_all(enriched_data)
        
        # Step 4: If conflicts exist, Conflict Resolution Agent resolves them
        violated = [c for c in constraints if c.violated]
        if violated:
            self.log_message("ConstraintAgent", "ConflictResolutionAgent", 
                           f"Found {len(violated)} violations")
            resolution = self.conflict_agent.resolve_conflicts(timetable, constraints)
            
            return {
                'status': 'conflicts_detected',
                'timetable': timetable,
                'constraints': [{'type': c.type, 'violated': c.violated, 'details': c.details} 
                              for c in constraints],
                'resolution': resolution,
                'message_log': self.message_log
            }
        
        # Step 5: Calculate utilization metrics
        utilization = self.optimization_agent.calculate_utilization(timetable)
        floor_optimization = self.resource_agent.optimize_floor_allocation(
            timetable, input_data.get('rooms', [])
        )
        
        return {
            'status': 'success',
            'timetable': timetable,
            'constraints': [{'type': c.type, 'violated': c.violated, 'details': c.details} 
                          for c in constraints],
            'utilization': utilization,
            'floor_optimization': floor_optimization,
            'message_log': self.message_log
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
