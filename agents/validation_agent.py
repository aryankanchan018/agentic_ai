"""Validation Agent for data validation"""
from typing import Dict, Any, List
from .base_agent import BaseAgent

class ValidationAgent(BaseAgent):
    """Agent responsible for validating input data before timetable generation"""
    
    def __init__(self):
        super().__init__("ValidationAgent")
        self.validation_rules = []
    
    def get_capabilities(self) -> list:
        return ['validate_data', 'check_completeness', 'verify_constraints']
    
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process validation request"""
        method = request.get('method')
        params = request.get('params', {})
        
        if method == 'validate_data':
            return self.validate_input_data(params)
        elif method == 'check_completeness':
            return self.check_data_completeness(params)
        elif method == 'verify_constraints':
            return self.verify_basic_constraints(params)
        
        return {'status': 'error', 'message': 'Unknown method'}
    
    def validate_input_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate input data structure and values"""
        errors = []
        warnings = []
        
        # Check divisions
        divisions = data.get('divisions', [])
        if not divisions:
            errors.append("No divisions provided")
        else:
            for div in divisions:
                if div.get('student_count', 0) <= 0:
                    errors.append(f"Division {div.get('name')} has invalid student count")
        
        # Check subjects
        subjects = data.get('subjects', [])
        if not subjects:
            errors.append("No subjects provided")
        else:
            for subj in subjects:
                if subj.get('hours_per_week', 0) <= 0:
                    errors.append(f"Subject {subj.get('name')} has invalid hours per week")
                if subj.get('hours_per_week', 0) > 10:
                    warnings.append(f"Subject {subj.get('name')} has unusually high hours ({subj.get('hours_per_week')})")
        
        # Check rooms
        rooms = data.get('rooms', [])
        if not rooms:
            errors.append("No rooms provided")
        else:
            for room in rooms:
                if room.get('capacity', 0) <= 0:
                    errors.append(f"Room {room.get('room_number')} has invalid capacity")
        
        # Check faculty
        faculty = data.get('faculty', [])
        if not faculty:
            errors.append("No faculty provided")
        
        # Check timeslots
        timeslots = data.get('timeslots', [])
        if not timeslots:
            errors.append("No timeslots provided")
        
        return {
            'status': 'valid' if not errors else 'invalid',
            'errors': errors,
            'warnings': warnings,
            'validated_by': self.agent_name
        }
    
    def check_data_completeness(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Check if all required data is present"""
        required_fields = ['divisions', 'subjects', 'rooms', 'faculty', 'timeslots']
        missing = [field for field in required_fields if not data.get(field)]
        
        # Check ratios
        divisions_count = len(data.get('divisions', []))
        rooms_count = len(data.get('rooms', []))
        faculty_count = len(data.get('faculty', []))
        
        suggestions = []
        if divisions_count > rooms_count:
            suggestions.append(f"Consider adding more rooms. Divisions: {divisions_count}, Rooms: {rooms_count}")
        if divisions_count > faculty_count:
            suggestions.append(f"Consider adding more faculty. Divisions: {divisions_count}, Faculty: {faculty_count}")
        
        return {
            'status': 'complete' if not missing else 'incomplete',
            'missing_fields': missing,
            'suggestions': suggestions,
            'checked_by': self.agent_name
        }
    
    def verify_basic_constraints(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Verify basic constraints are satisfiable"""
        issues = []
        
        divisions = data.get('divisions', [])
        rooms = data.get('rooms', [])
        subjects = data.get('subjects', [])
        
        # Check if there are enough lab rooms for lab subjects
        lab_subjects = [s for s in subjects if s.get('is_lab', False)]
        lab_rooms = [r for r in rooms if r.get('is_lab', False)]
        
        if lab_subjects and not lab_rooms:
            issues.append("Lab subjects exist but no lab rooms available")
        
        # Check if rooms can accommodate divisions
        max_students = max([d.get('student_count', 0) for d in divisions], default=0)
        max_capacity = max([r.get('capacity', 0) for r in rooms], default=0)
        
        if max_students > max_capacity:
            issues.append(f"Largest division ({max_students} students) exceeds largest room capacity ({max_capacity})")
        
        # Check total hours feasibility
        total_hours_needed = sum([s.get('hours_per_week', 0) for s in subjects]) * len(divisions)
        total_slots_available = len(data.get('timeslots', []))
        
        if total_hours_needed > total_slots_available:
            issues.append(f"Total hours needed ({total_hours_needed}) exceeds available slots ({total_slots_available})")
        
        return {
            'status': 'feasible' if not issues else 'potential_issues',
            'issues': issues,
            'verified_by': self.agent_name
        }
