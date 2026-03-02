from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class Constraint:
    type: str
    description: str
    violated: bool
    details: str

class ConstraintAgent:
    """Agent responsible for validating timetable constraints"""
    
    def __init__(self):
        self.name = "ConstraintAgent"
        self.constraints = []
    
    def check_room_capacity(self, room_capacity: int, student_count: int) -> Constraint:
        violated = student_count > room_capacity
        return Constraint(
            type="room_capacity",
            description="Room capacity must accommodate all students",
            violated=violated,
            details=f"Room: {room_capacity}, Students: {student_count}"
        )
    
    def check_faculty_overlap(self, faculty_schedule: Dict) -> Constraint:
        """Check if faculty is assigned to multiple classes at same time"""
        violations = []
        for timeslot, assignments in faculty_schedule.items():
            if len(assignments) > 1:
                violations.append(f"Timeslot {timeslot}: {len(assignments)} assignments")
        
        return Constraint(
            type="faculty_overlap",
            description="Faculty cannot teach multiple classes simultaneously",
            violated=len(violations) > 0,
            details="; ".join(violations) if violations else "No violations"
        )
    
    def check_room_overlap(self, room_schedule: Dict) -> Constraint:
        """Check if room is assigned to multiple classes at same time"""
        violations = []
        for timeslot, assignments in room_schedule.items():
            if len(assignments) > 1:
                violations.append(f"Timeslot {timeslot}: {len(assignments)} assignments")
        
        return Constraint(
            type="room_overlap",
            description="Room cannot host multiple classes simultaneously",
            violated=len(violations) > 0,
            details="; ".join(violations) if violations else "No violations"
        )
    
    def check_division_overlap(self, division_schedule: Dict) -> Constraint:
        """Check if division has multiple classes at same time"""
        violations = []
        for timeslot, assignments in division_schedule.items():
            if len(assignments) > 1:
                violations.append(f"Timeslot {timeslot}: {len(assignments)} classes")
        
        return Constraint(
            type="division_overlap",
            description="Division cannot attend multiple classes simultaneously",
            violated=len(violations) > 0,
            details="; ".join(violations) if violations else "No violations"
        )
    
    def check_lab_requirements(self, subject_is_lab: bool, room_is_lab: bool) -> Constraint:
        violated = subject_is_lab and not room_is_lab
        return Constraint(
            type="lab_requirement",
            description="Lab subjects must be assigned to lab rooms",
            violated=violated,
            details=f"Subject is lab: {subject_is_lab}, Room is lab: {room_is_lab}"
        )
    
    def validate_all(self, timetable_data: Dict) -> List[Constraint]:
        """Run all constraint checks"""
        results = []
        
        # Build schedules for overlap checking
        faculty_schedule = {}
        room_schedule = {}
        division_schedule = {}
        
        for entry in timetable_data.get('entries', []):
            timeslot = entry['timeslot_id']
            
            faculty_schedule.setdefault(timeslot, []).append(entry['faculty_id'])
            room_schedule.setdefault(timeslot, []).append(entry['room_id'])
            division_schedule.setdefault(timeslot, []).append(entry['division_id'])
            
            # Check capacity and lab requirements
            results.append(self.check_room_capacity(
                entry.get('room_capacity', 0),
                entry.get('student_count', 0)
            ))
            results.append(self.check_lab_requirements(
                entry.get('subject_is_lab', False),
                entry.get('room_is_lab', False)
            ))
        
        # Check overlaps
        results.append(self.check_faculty_overlap(faculty_schedule))
        results.append(self.check_room_overlap(room_schedule))
        results.append(self.check_division_overlap(division_schedule))
        
        return results
