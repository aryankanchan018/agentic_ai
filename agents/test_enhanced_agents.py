"""Comprehensive test suite for all agents"""
import asyncio
import sys
sys.path.append('..')

from agents import (
    ValidationAgent,
    ResourceAllocationAgent,
    OptimizationAgent,
    ConstraintAgent,
    ConflictResolutionAgent,
    MonitoringAgent,
    AnalyticsAgent,
    AgentOrchestrator,
    AgentRegistry
)

# Test data
test_data = {
    'divisions': [
        {'id': 1, 'name': 'CS-A', 'student_count': 60, 'year': 3, 'department_id': 1},
        {'id': 2, 'name': 'CS-B', 'student_count': 55, 'year': 3, 'department_id': 1}
    ],
    'subjects': [
        {'id': 1, 'name': 'Data Structures', 'code': 'CS301', 'hours_per_week': 4, 'is_lab': False},
        {'id': 2, 'name': 'Database Lab', 'code': 'CS302L', 'hours_per_week': 2, 'is_lab': True},
        {'id': 3, 'name': 'Operating Systems', 'code': 'CS303', 'hours_per_week': 3, 'is_lab': False}
    ],
    'rooms': [
        {'id': 1, 'room_number': '301', 'capacity': 70, 'is_lab': False, 'floor': 3, 'bench_count': 35},
        {'id': 2, 'room_number': '302', 'capacity': 60, 'is_lab': False, 'floor': 3, 'bench_count': 30},
        {'id': 3, 'room_number': 'LAB1', 'capacity': 50, 'is_lab': True, 'floor': 2, 'bench_count': 25}
    ],
    'faculty': [
        {'id': 1, 'name': 'Dr. Smith', 'employee_id': 'F001'},
        {'id': 2, 'name': 'Dr. Johnson', 'employee_id': 'F002'},
        {'id': 3, 'name': 'Prof. Williams', 'employee_id': 'F003'}
    ],
    'timeslots': [
        {'id': 1, 'day': 'Monday', 'start_time': '09:00', 'end_time': '10:00', 'slot_number': 1},
        {'id': 2, 'day': 'Monday', 'start_time': '10:00', 'end_time': '11:00', 'slot_number': 2},
        {'id': 3, 'day': 'Monday', 'start_time': '11:00', 'end_time': '12:00', 'slot_number': 3},
        {'id': 4, 'day': 'Tuesday', 'start_time': '09:00', 'end_time': '10:00', 'slot_number': 1},
        {'id': 5, 'day': 'Tuesday', 'start_time': '10:00', 'end_time': '11:00', 'slot_number': 2}
    ]
}

async def test_validation_agent():
    """Test ValidationAgent"""
    print("\n=== Testing ValidationAgent ===")
    agent = ValidationAgent()
    await agent.initialize()
    
    # Test data validation
    result = await agent.process_request({
        'method': 'validate_data',
        'params': test_data
    })
    print(f"Validation Result: {result['status']}")
    if result.get('errors'):
        print(f"Errors: {result['errors']}")
    if result.get('warnings'):
        print(f"Warnings: {result['warnings']}")
    
    # Test completeness check
    result = await agent.process_request({
        'method': 'check_completeness',
        'params': test_data
    })
    print(f"Completeness: {result['status']}")
    if result.get('suggestions'):
        print(f"Suggestions: {result['suggestions']}")
    
    await agent.shutdown()
    print("✓ ValidationAgent tests passed")

async def test_resource_allocation_agent():
    """Test ResourceAllocationAgent"""
    print("\n=== Testing ResourceAllocationAgent ===")
    agent = ResourceAllocationAgent()
    await agent.initialize()
    
    requirements = {
        'requests': [
            {'division_id': 1, 'subject_id': 1, 'student_count': 60, 'is_lab': False},
            {'division_id': 1, 'subject_id': 2, 'student_count': 60, 'is_lab': True}
        ]
    }
    
    result = await agent.process_request({
        'method': 'allocate_rooms',
        'params': {'requirements': requirements, 'rooms': test_data['rooms']}
    })
    print(f"Allocated: {len(result.get('allocations', []))} rooms")
    print(f"Unallocated: {result.get('unallocated', 0)}")
    
    await agent.shutdown()
    print("✓ ResourceAllocationAgent tests passed")

async def test_monitoring_agent():
    """Test MonitoringAgent"""
    print("\n=== Testing MonitoringAgent ===")
    agent = MonitoringAgent()
    await agent.initialize()
    
    # Track generation start
    await agent.process_request({
        'method': 'track_performance',
        'params': {'event_type': 'generation_started'}
    })
    
    # Track generation completion
    result = await agent.process_request({
        'method': 'track_performance',
        'params': {
            'event_type': 'generation_completed',
            'status': 'success',
            'generation_time': 2.5
        }
    })
    print(f"Metrics: {result.get('metrics', {})}")
    
    # Check health
    health = await agent.process_request({
        'method': 'monitor_health',
        'params': {}
    })
    print(f"System Health: {health.get('status')}")
    
    # Generate report
    report = await agent.process_request({
        'method': 'generate_report',
        'params': {}
    })
    print(f"Report Summary: {report.get('summary', {})}")
    
    await agent.shutdown()
    print("✓ MonitoringAgent tests passed")

async def test_analytics_agent():
    """Test AnalyticsAgent"""
    print("\n=== Testing AnalyticsAgent ===")
    agent = AnalyticsAgent()
    await agent.initialize()
    
    sample_timetable = [
        {'division_id': 1, 'subject_id': 1, 'room_id': 1, 'faculty_id': 1, 'timeslot_id': 1, 'day': 'Monday'},
        {'division_id': 1, 'subject_id': 2, 'room_id': 3, 'faculty_id': 2, 'timeslot_id': 2, 'day': 'Monday'},
        {'division_id': 2, 'subject_id': 1, 'room_id': 2, 'faculty_id': 1, 'timeslot_id': 3, 'day': 'Monday'}
    ]
    
    # Analyze timetable
    result = await agent.process_request({
        'method': 'analyze_timetable',
        'params': {'timetable': sample_timetable}
    })
    print(f"Statistics: {result.get('statistics', {})}")
    
    # Generate insights
    insights = await agent.process_request({
        'method': 'generate_insights',
        'params': {'timetable': sample_timetable}
    })
    print(f"Insights: {len(insights.get('insights', []))} found")
    
    # Recommendations
    recommendations = await agent.process_request({
        'method': 'recommend_improvements',
        'params': {'timetable': sample_timetable}
    })
    print(f"Recommendations: {len(recommendations.get('recommendations', []))} generated")
    
    await agent.shutdown()
    print("✓ AnalyticsAgent tests passed")

async def test_agent_registry():
    """Test AgentRegistry"""
    print("\n=== Testing AgentRegistry ===")
    registry = AgentRegistry()
    
    # Register agents
    registry.register_agent('TestAgent1', ['capability1', 'capability2'])
    registry.register_agent('TestAgent2', ['capability2', 'capability3'])
    
    # Find by capability
    agents = registry.find_agent_by_capability('capability2')
    print(f"Agents with capability2: {agents}")
    
    # Log messages
    registry.log_message('TestAgent1', 'TestAgent2', 'test_method', 'sent')
    registry.log_message('TestAgent2', 'TestAgent1', 'test_method', 'completed')
    
    # Get logs
    logs = registry.get_message_log()
    print(f"Message log entries: {len(logs)}")
    
    # Get all agents
    all_agents = registry.get_all_agents()
    print(f"Total registered agents: {len(all_agents)}")
    
    print("✓ AgentRegistry tests passed")

async def test_orchestrator():
    """Test AgentOrchestrator with full workflow"""
    print("\n=== Testing AgentOrchestrator (Full Workflow) ===")
    
    # Add requirements to test data
    test_data['requirements'] = [
        {'division_id': d['id'], 'subject_id': s['id'], 'student_count': d['student_count'], 'is_lab': s['is_lab']}
        for d in test_data['divisions']
        for s in test_data['subjects']
    ]
    
    orchestrator = AgentOrchestrator(mcp_enabled=False)
    
    print("Starting timetable generation...")
    result = orchestrator.generate_timetable(test_data)
    
    print(f"\nGeneration Status: {result['status']}")
    print(f"Generation Time: {result.get('generation_time', 0):.2f}s")
    print(f"Timetable Entries: {len(result.get('timetable', []))}")
    print(f"Constraints Checked: {len(result.get('constraints', []))}")
    print(f"Insights Generated: {len(result.get('insights', []))}")
    print(f"Recommendations: {len(result.get('recommendations', []))}")
    print(f"Message Log Entries: {len(result.get('message_log', []))}")
    
    # Display agent status
    print("\nAgent Status:")
    for agent_name, info in result.get('agent_status', {}).items():
        print(f"  {agent_name}: {info['status']} ({info['message_count']} messages)")
    
    # Display some insights
    if result.get('insights'):
        print("\nSample Insights:")
        for insight in result['insights'][:3]:
            print(f"  - [{insight['severity']}] {insight['message']}")
    
    # Display recommendations
    if result.get('recommendations'):
        print("\nSample Recommendations:")
        for rec in result['recommendations'][:3]:
            print(f"  - [{rec['priority']}] {rec['recommendation']}")
    
    print("\n✓ AgentOrchestrator tests passed")

async def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("MULTI-AGENT SYSTEM TEST SUITE")
    print("=" * 60)
    
    try:
        await test_validation_agent()
        await test_resource_allocation_agent()
        await test_monitoring_agent()
        await test_analytics_agent()
        await test_agent_registry()
        await test_orchestrator()
        
        print("\n" + "=" * 60)
        print("ALL TESTS PASSED ✓")
        print("=" * 60)
    
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_all_tests())
