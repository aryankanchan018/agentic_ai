from typing import List, Dict, Any

class ResourceAllocationAgent:
    """Agent responsible for managing resource allocation"""
    
    def __init__(self):
        self.name = "ResourceAllocationAgent"
    
    def allocate_rooms(self, requirements: Dict, available_rooms: List[Dict]) -> Dict:
        """Allocate rooms based on requirements"""
        allocations = []
        
        for req in requirements.get('requests', []):
            student_count = req['student_count']
            is_lab = req['is_lab']
            
            # Find suitable room
            suitable_rooms = [
                r for r in available_rooms
                if r['capacity'] >= student_count
                and r['is_lab'] == is_lab
                and r['id'] not in [a['room_id'] for a in allocations]
            ]
            
            if suitable_rooms:
                # Select room with closest capacity match
                best_room = min(suitable_rooms, key=lambda r: r['capacity'] - student_count)
                allocations.append({
                    'division_id': req['division_id'],
                    'subject_id': req['subject_id'],
                    'room_id': best_room['id'],
                    'room_number': best_room['room_number']
                })
        
        return {
            'allocations': allocations,
            'unallocated': len(requirements.get('requests', [])) - len(allocations)
        }
    
    def check_bench_availability(self, room: Dict, student_count: int) -> bool:
        """Check if room has enough benches"""
        students_per_bench = 2  # Typical
        required_benches = (student_count + students_per_bench - 1) // students_per_bench
        return room.get('bench_count', 0) >= required_benches
    
    def optimize_floor_allocation(self, allocations: List[Dict], rooms: List[Dict]) -> Dict:
        """Optimize to minimize floor changes for divisions"""
        floor_usage = {}
        
        for alloc in allocations:
            division_id = alloc['division_id']
            room = next((r for r in rooms if r['id'] == alloc['room_id']), None)
            
            if room:
                floor = room['floor']
                if division_id not in floor_usage:
                    floor_usage[division_id] = {}
                floor_usage[division_id][floor] = floor_usage[division_id].get(floor, 0) + 1
        
        # Calculate floor change score (lower is better)
        floor_changes = 0
        for division_id, floors in floor_usage.items():
            if len(floors) > 1:
                floor_changes += len(floors) - 1
        
        return {
            'floor_changes': floor_changes,
            'floor_usage': floor_usage,
            'optimization_score': 100 - (floor_changes * 10)  # Simple scoring
        }
