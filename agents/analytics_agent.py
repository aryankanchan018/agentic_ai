"""Analytics Agent for insights and recommendations"""
from typing import Dict, Any, List
from collections import Counter
from .base_agent import BaseAgent

class AnalyticsAgent(BaseAgent):
    """Agent responsible for analyzing timetables and providing insights"""
    
    def __init__(self):
        super().__init__("AnalyticsAgent")
    
    def get_capabilities(self) -> list:
        return ['analyze_timetable', 'generate_insights', 'recommend_improvements']
    
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process analytics request"""
        method = request.get('method')
        params = request.get('params', {})
        
        if method == 'analyze_timetable':
            return self.analyze_timetable(params)
        elif method == 'generate_insights':
            return self.generate_insights(params)
        elif method == 'recommend_improvements':
            return self.recommend_improvements(params)
        
        return {'status': 'error', 'message': 'Unknown method'}
    
    def analyze_timetable(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze timetable for patterns and statistics"""
        timetable = data.get('timetable', [])
        
        if not timetable:
            return {'status': 'no_data', 'message': 'No timetable data provided'}
        
        # Analyze distribution
        day_distribution = Counter([entry.get('day') for entry in timetable])
        room_usage = Counter([entry.get('room_id') for entry in timetable])
        faculty_load = Counter([entry.get('faculty_id') for entry in timetable])
        division_schedule = Counter([entry.get('division_id') for entry in timetable])
        
        # Calculate balance metrics
        room_usage_values = list(room_usage.values())
        room_balance = (
            max(room_usage_values) - min(room_usage_values) 
            if room_usage_values else 0
        )
        
        faculty_load_values = list(faculty_load.values())
        faculty_balance = (
            max(faculty_load_values) - min(faculty_load_values)
            if faculty_load_values else 0
        )
        
        return {
            'status': 'analyzed',
            'statistics': {
                'total_classes': len(timetable),
                'unique_rooms': len(room_usage),
                'unique_faculty': len(faculty_load),
                'unique_divisions': len(division_schedule),
                'day_distribution': dict(day_distribution),
                'room_balance_score': 100 - (room_balance * 5),
                'faculty_balance_score': 100 - (faculty_balance * 5)
            },
            'analyzed_by': self.agent_name
        }
    
    def generate_insights(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate insights from timetable analysis"""
        timetable = data.get('timetable', [])
        insights = []
        
        if not timetable:
            return {'status': 'no_data', 'insights': []}
        
        # Check for gaps in division schedules
        division_schedules = {}
        for entry in timetable:
            div_id = entry.get('division_id')
            day = entry.get('day')
            timeslot = entry.get('timeslot_id')
            
            if div_id not in division_schedules:
                division_schedules[div_id] = {}
            if day not in division_schedules[div_id]:
                division_schedules[div_id][day] = []
            division_schedules[div_id][day].append(timeslot)
        
        # Analyze gaps
        for div_id, days in division_schedules.items():
            for day, slots in days.items():
                sorted_slots = sorted(slots)
                gaps = []
                for i in range(len(sorted_slots) - 1):
                    if sorted_slots[i+1] - sorted_slots[i] > 1:
                        gaps.append((sorted_slots[i], sorted_slots[i+1]))
                
                if gaps:
                    insights.append({
                        'type': 'schedule_gap',
                        'severity': 'medium',
                        'message': f"Division {div_id} has {len(gaps)} gap(s) on {day}",
                        'details': gaps
                    })
        
        # Check room utilization
        room_usage = Counter([entry.get('room_id') for entry in timetable])
        avg_usage = sum(room_usage.values()) / len(room_usage) if room_usage else 0
        
        for room_id, usage in room_usage.items():
            if usage < avg_usage * 0.5:
                insights.append({
                    'type': 'underutilized_room',
                    'severity': 'low',
                    'message': f"Room {room_id} is underutilized ({usage} classes)",
                    'details': {'room_id': room_id, 'usage': usage, 'average': avg_usage}
                })
            elif usage > avg_usage * 1.5:
                insights.append({
                    'type': 'overutilized_room',
                    'severity': 'medium',
                    'message': f"Room {room_id} is heavily used ({usage} classes)",
                    'details': {'room_id': room_id, 'usage': usage, 'average': avg_usage}
                })
        
        # Check faculty load balance
        faculty_load = Counter([entry.get('faculty_id') for entry in timetable])
        avg_load = sum(faculty_load.values()) / len(faculty_load) if faculty_load else 0
        
        for faculty_id, load in faculty_load.items():
            if load > avg_load * 1.5:
                insights.append({
                    'type': 'high_faculty_load',
                    'severity': 'high',
                    'message': f"Faculty {faculty_id} has high teaching load ({load} classes)",
                    'details': {'faculty_id': faculty_id, 'load': load, 'average': avg_load}
                })
        
        return {
            'status': 'insights_generated',
            'insights': insights,
            'total_insights': len(insights),
            'generated_by': self.agent_name
        }
    
    def recommend_improvements(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend improvements based on analysis"""
        timetable = data.get('timetable', [])
        recommendations = []
        
        if not timetable:
            return {'status': 'no_data', 'recommendations': []}
        
        # Analyze and recommend
        room_usage = Counter([entry.get('room_id') for entry in timetable])
        faculty_load = Counter([entry.get('faculty_id') for entry in timetable])
        
        # Room recommendations
        if len(room_usage) > 0:
            usage_values = list(room_usage.values())
            if max(usage_values) - min(usage_values) > 5:
                recommendations.append({
                    'category': 'resource_balancing',
                    'priority': 'medium',
                    'recommendation': 'Balance room usage more evenly across available rooms',
                    'expected_benefit': 'Reduced wear on heavily used rooms, better resource distribution'
                })
        
        # Faculty recommendations
        if len(faculty_load) > 0:
            load_values = list(faculty_load.values())
            if max(load_values) - min(load_values) > 5:
                recommendations.append({
                    'category': 'workload_balancing',
                    'priority': 'high',
                    'recommendation': 'Redistribute teaching load more evenly among faculty',
                    'expected_benefit': 'Improved faculty satisfaction, reduced burnout risk'
                })
        
        # Check for consecutive classes
        division_schedules = {}
        for entry in timetable:
            div_id = entry.get('division_id')
            day = entry.get('day')
            timeslot = entry.get('timeslot_id')
            
            if div_id not in division_schedules:
                division_schedules[div_id] = {}
            if day not in division_schedules[div_id]:
                division_schedules[div_id][day] = []
            division_schedules[div_id][day].append(timeslot)
        
        for div_id, days in division_schedules.items():
            for day, slots in days.items():
                sorted_slots = sorted(slots)
                consecutive_count = 1
                max_consecutive = 1
                
                for i in range(len(sorted_slots) - 1):
                    if sorted_slots[i+1] - sorted_slots[i] == 1:
                        consecutive_count += 1
                        max_consecutive = max(max_consecutive, consecutive_count)
                    else:
                        consecutive_count = 1
                
                if max_consecutive > 4:
                    recommendations.append({
                        'category': 'schedule_optimization',
                        'priority': 'medium',
                        'recommendation': f'Reduce consecutive classes for division {div_id} on {day}',
                        'expected_benefit': 'Improved student attention and learning outcomes'
                    })
        
        return {
            'status': 'recommendations_generated',
            'recommendations': recommendations,
            'total_recommendations': len(recommendations),
            'generated_by': self.agent_name
        }
