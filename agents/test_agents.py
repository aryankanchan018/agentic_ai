import sys
sys.path.append('..')
from agents.constraint_agent import ConstraintAgent
from agents.optimization_agent import OptimizationAgent
from agents.resource_allocation_agent import ResourceAllocationAgent
from agents.orchestrator import AgentOrchestrator

def test_constraint_agent():
    print("Testing Constraint Agent...")
    agent = ConstraintAgent()
    
    # Test room capacity
    result = agent.check_room_capacity(50, 55)
    print(f"  Room capacity check: {'PASS' if result.violated else 'FAIL'}")
    
    # Test faculty overlap
    schedule = {1: [1, 2], 2: [1]}  # Faculty 1 has 2 classes at timeslot 1
    result = agent.check_faculty_overlap(schedule)
    print(f"  Faculty overlap check: {'PASS' if result.violated else 'FAIL'}")
    
    print("✓ Constraint Agent tests passed\n")

def test_resource_allocation_agent():
    print("Testing Resource Allocation Agent...")
    agent = ResourceAllocationAgent()
    
    requirements = {
        'requests': [
            {'division_id': 1, 'subject_id': 1, 'student_count': 50, 'is_lab': False},
            {'division_id': 2, 'subject_id': 2, 'student_count': 30, 'is_lab': True}
        ]
    }
    
    rooms = [
        {'id': 1, 'room_number': '101', 'capacity': 60, 'is_lab': False},
        {'id': 2, 'room_number': '201', 'capacity': 40, 'is_lab': True}
    ]
    
    result = agent.allocate_rooms(requirements, rooms)
    print(f"  Allocated: {len(result['allocations'])} rooms")
    print(f"  Unallocated: {result['unallocated']}")
    print("✓ Resource Allocation Agent tests passed\n")

def test_optimization_agent():
    print("Testing Optimization Agent...")
    agent = OptimizationAgent()
    
    timetable = [
        {'division_id': 1, 'subject_id': 1, 'room_id': 1, 'faculty_id': 1, 'timeslot_id': 1},
        {'division_id': 1, 'subject_id': 2, 'room_id': 2, 'faculty_id': 2, 'timeslot_id': 2},
    ]
    
    utilization = agent.calculate_utilization(timetable)
    print(f"  Total classes: {utilization['total_classes']}")
    print(f"  Slot utilization: {utilization['slot_utilization']:.2%}")
    print("✓ Optimization Agent tests passed\n")

def test_orchestrator():
    print("Testing Agent Orchestrator...")
    orchestrator = AgentOrchestrator()
    
    # Minimal test data
    input_data = {
        'divisions': [{'id': 1, 'name': 'CS-A', 'student_count': 50}],
        'subjects': [{'id': 1, 'name': 'DS', 'hours_per_week': 2, 'is_lab': False}],
        'rooms': [{'id': 1, 'room_number': '101', 'capacity': 60, 'is_lab': False, 'floor': 1, 'bench_count': 30}],
        'faculty': [{'id': 1, 'name': 'Dr. Smith'}],
        'timeslots': [
            {'id': 1, 'day': 0, 'slot_number': 1},
            {'id': 2, 'day': 0, 'slot_number': 2}
        ],
        'requirements': [
            {'division_id': 1, 'subject_id': 1, 'student_count': 50, 'is_lab': False}
        ]
    }
    
    result = orchestrator.generate_timetable(input_data)
    print(f"  Status: {result['status']}")
    print(f"  A2A messages: {len(result.get('message_log', []))}")
    
    if result.get('message_log'):
        print("  Agent communication:")
        for msg in result['message_log'][:3]:
            print(f"    {msg['sender']} → {msg['receiver']}: {msg['message']}")
    
    print("✓ Orchestrator tests passed\n")

if __name__ == "__main__":
    print("=" * 50)
    print("Agent System Test Suite")
    print("=" * 50 + "\n")
    
    test_constraint_agent()
    test_resource_allocation_agent()
    test_optimization_agent()
    test_orchestrator()
    
    print("=" * 50)
    print("All tests completed successfully!")
    print("=" * 50)
