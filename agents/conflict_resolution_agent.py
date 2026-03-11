from typing import List, Dict, Any
import random
from .base_agent import BaseAgent

class ConflictResolutionAgent(BaseAgent):
    """Agent responsible for resolving scheduling conflicts"""
    
    def __init__(self):
        super().__init__("ConflictResolutionAgent")
    
    def get_capabilities(self) -> list:
        return ['resolve_conflicts', 'suggest_alternatives', 'apply_resolution']
    
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process conflict resolution request"""
        method = request.get('method')
        params = request.get('params', {})
        
        if method == 'resolve_conflicts':
            result = self.resolve_conflicts(params.get('timetable', []), params.get('constraints', []))
            return result
        
        return {'status': 'error', 'message': 'Unknown method'}
    
    def resolve_conflicts(self, timetable: List[Dict], constraints: List[Any]) -> Dict:
        """Attempt to resolve conflicts in timetable"""
        violated_constraints = [c for c in constraints if c.violated]
        
        if not violated_constraints:
            return {'status': 'no_conflicts', 'timetable': timetable}
        
        resolution_strategies = []
        
        for constraint in violated_constraints:
            if constraint.type == 'faculty_overlap':
                strategy = self._resolve_faculty_overlap(timetable)
                resolution_strategies.append(strategy)
            
            elif constraint.type == 'room_overlap':
                strategy = self._resolve_room_overlap(timetable)
                resolution_strategies.append(strategy)
            
            elif constraint.type == 'division_overlap':
                strategy = self._resolve_division_overlap(timetable)
                resolution_strategies.append(strategy)
            
            elif constraint.type == 'room_capacity':
                strategy = self._resolve_capacity_issue(timetable)
                resolution_strategies.append(strategy)
        
        return {
            'status': 'conflicts_found',
            'violated_constraints': len(violated_constraints),
            'resolution_strategies': resolution_strategies
        }
    
    def _resolve_faculty_overlap(self, timetable: List[Dict]) -> Dict:
        """Suggest moving one class to different timeslot"""
        return {
            'type': 'faculty_overlap',
            'action': 'reschedule',
            'suggestion': 'Move conflicting class to available timeslot'
        }
    
    def _resolve_room_overlap(self, timetable: List[Dict]) -> Dict:
        """Suggest alternative room or timeslot"""
        return {
            'type': 'room_overlap',
            'action': 'reassign_room',
            'suggestion': 'Assign to alternative available room'
        }
    
    def _resolve_division_overlap(self, timetable: List[Dict]) -> Dict:
        """Suggest rescheduling one of the classes"""
        return {
            'type': 'division_overlap',
            'action': 'reschedule',
            'suggestion': 'Reschedule one class to different timeslot'
        }
    
    def _resolve_capacity_issue(self, timetable: List[Dict]) -> Dict:
        """Suggest larger room"""
        return {
            'type': 'room_capacity',
            'action': 'reassign_room',
            'suggestion': 'Assign to larger capacity room'
        }
    
    def apply_resolution(self, timetable: List[Dict], strategy: Dict) -> List[Dict]:
        """Apply resolution strategy to timetable"""
        # Implementation would modify timetable based on strategy
        return timetable
