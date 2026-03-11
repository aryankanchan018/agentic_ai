"""Monitoring Agent for system health and performance tracking"""
from typing import Dict, Any, List
from datetime import datetime
from .base_agent import BaseAgent

class MonitoringAgent(BaseAgent):
    """Agent responsible for monitoring system health and performance"""
    
    def __init__(self):
        super().__init__("MonitoringAgent")
        self.metrics = {
            'timetable_generations': 0,
            'successful_generations': 0,
            'failed_generations': 0,
            'average_generation_time': 0,
            'constraint_violations': 0,
            'conflicts_resolved': 0
        }
        self.performance_log = []
    
    def get_capabilities(self) -> list:
        return ['track_performance', 'monitor_health', 'generate_report']
    
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process monitoring request"""
        method = request.get('method')
        params = request.get('params', {})
        
        if method == 'track_performance':
            return self.track_performance(params)
        elif method == 'monitor_health':
            return self.check_system_health(params)
        elif method == 'generate_report':
            return self.generate_performance_report()
        
        return {'status': 'error', 'message': 'Unknown method'}
    
    def track_performance(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Track performance metrics"""
        event_type = data.get('event_type')
        
        if event_type == 'generation_started':
            self.metrics['timetable_generations'] += 1
        
        elif event_type == 'generation_completed':
            status = data.get('status')
            if status == 'success':
                self.metrics['successful_generations'] += 1
            else:
                self.metrics['failed_generations'] += 1
            
            # Track generation time
            generation_time = data.get('generation_time', 0)
            current_avg = self.metrics['average_generation_time']
            total_gens = self.metrics['timetable_generations']
            self.metrics['average_generation_time'] = (
                (current_avg * (total_gens - 1) + generation_time) / total_gens
            )
        
        elif event_type == 'constraint_violation':
            self.metrics['constraint_violations'] += 1
        
        elif event_type == 'conflict_resolved':
            self.metrics['conflicts_resolved'] += 1
        
        # Log event
        self.performance_log.append({
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'data': data
        })
        
        return {
            'status': 'tracked',
            'metrics': self.metrics,
            'tracked_by': self.agent_name
        }
    
    def check_system_health(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Check overall system health"""
        health_status = 'healthy'
        issues = []
        
        # Check success rate
        total_gens = self.metrics['timetable_generations']
        if total_gens > 0:
            success_rate = self.metrics['successful_generations'] / total_gens
            if success_rate < 0.5:
                health_status = 'degraded'
                issues.append(f"Low success rate: {success_rate:.2%}")
        
        # Check average generation time
        avg_time = self.metrics['average_generation_time']
        if avg_time > 30:
            health_status = 'degraded'
            issues.append(f"High average generation time: {avg_time:.2f}s")
        
        # Check constraint violations
        if self.metrics['constraint_violations'] > 10:
            issues.append(f"High constraint violations: {self.metrics['constraint_violations']}")
        
        return {
            'status': health_status,
            'issues': issues,
            'metrics': self.metrics,
            'checked_by': self.agent_name,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def generate_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        total_gens = self.metrics['timetable_generations']
        success_rate = (
            self.metrics['successful_generations'] / total_gens 
            if total_gens > 0 else 0
        )
        
        return {
            'report_type': 'performance',
            'generated_at': datetime.utcnow().isoformat(),
            'summary': {
                'total_generations': total_gens,
                'successful': self.metrics['successful_generations'],
                'failed': self.metrics['failed_generations'],
                'success_rate': f"{success_rate:.2%}",
                'average_time': f"{self.metrics['average_generation_time']:.2f}s",
                'constraint_violations': self.metrics['constraint_violations'],
                'conflicts_resolved': self.metrics['conflicts_resolved']
            },
            'recent_events': self.performance_log[-20:],
            'generated_by': self.agent_name
        }
    
    def reset_metrics(self):
        """Reset all metrics"""
        self.metrics = {
            'timetable_generations': 0,
            'successful_generations': 0,
            'failed_generations': 0,
            'average_generation_time': 0,
            'constraint_violations': 0,
            'conflicts_resolved': 0
        }
        self.performance_log = []
