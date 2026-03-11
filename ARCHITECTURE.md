# Enhanced Multi-Agent Architecture

## Overview

This project implements a sophisticated multi-agent system for university timetable generation using:
- **MCP (Model Context Protocol)** for standardized agent communication
- **A2A (Agent-to-Agent)** messaging for distributed coordination
- **8 Specialized Agents** working collaboratively
- **Agent Registry** for service discovery
- **Real-time monitoring** and analytics

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent Orchestrator                        │
│              (Coordinates all agent activities)              │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │      Agent Registry          │
        │  (Service Discovery & Logs)  │
        └──────────────┬──────────────┘
                       │
    ┌──────────────────┼──────────────────┐
    │                  │                   │
┌───▼────┐      ┌─────▼──────┐     ┌─────▼──────┐
│  MCP   │◄────►│   Agents   │◄───►│  Backend   │
│ Server │      │  (8 types) │     │   (API)    │
└────────┘      └────────────┘     └────────────┘
```

## Agents

### 1. ValidationAgent
**Capabilities:** `validate_data`, `check_completeness`, `verify_constraints`

**Responsibilities:**
- Validates input data structure and values
- Checks data completeness
- Verifies basic constraint satisfiability
- Pre-flight checks before timetable generation

**Methods:**
- `validate_input_data()` - Validates divisions, subjects, rooms, faculty, timeslots
- `check_data_completeness()` - Ensures all required data present
- `verify_basic_constraints()` - Checks if constraints are satisfiable

### 2. ResourceAllocationAgent
**Capabilities:** `allocate_rooms`, `optimize_floor_allocation`, `check_bench_availability`

**Responsibilities:**
- Allocates rooms based on requirements
- Optimizes floor allocation to minimize movement
- Checks bench availability
- Manages physical resource constraints

**Methods:**
- `allocate_rooms()` - Matches rooms to requirements
- `optimize_floor_allocation()` - Minimizes floor changes
- `check_bench_availability()` - Verifies seating capacity

### 3. OptimizationAgent
**Capabilities:** `optimize_timetable`, `calculate_utilization`, `solve_constraints`

**Responsibilities:**
- Uses OR-Tools CP-SAT solver for optimization
- Generates optimal timetable assignments
- Minimizes gaps in schedules
- Maximizes resource utilization
- Calculates utilization metrics

**Methods:**
- `optimize_timetable()` - Main constraint programming solver
- `calculate_utilization()` - Computes resource usage metrics

### 4. ConstraintAgent
**Capabilities:** `validate_constraints`, `check_capacity`, `check_overlaps`

**Responsibilities:**
- Validates all timetable constraints
- Checks room capacity constraints
- Detects faculty/room/division overlaps
- Verifies lab requirements

**Methods:**
- `validate_all()` - Runs all constraint checks
- `check_room_capacity()` - Validates capacity
- `check_faculty_overlap()` - Detects scheduling conflicts
- `check_lab_requirements()` - Ensures lab subjects in lab rooms

### 5. ConflictResolutionAgent
**Capabilities:** `resolve_conflicts`, `suggest_alternatives`, `apply_resolution`

**Responsibilities:**
- Resolves scheduling conflicts
- Suggests alternative timeslots/rooms
- Applies resolution strategies
- Handles constraint violations

**Methods:**
- `resolve_conflicts()` - Main conflict resolution
- `_resolve_faculty_overlap()` - Handles faculty conflicts
- `_resolve_room_overlap()` - Handles room conflicts

### 6. MonitoringAgent
**Capabilities:** `track_performance`, `monitor_health`, `generate_report`

**Responsibilities:**
- Tracks system performance metrics
- Monitors generation success rates
- Detects system health issues
- Generates performance reports

**Methods:**
- `track_performance()` - Logs performance events
- `check_system_health()` - Evaluates system status
- `generate_performance_report()` - Creates comprehensive reports

### 7. AnalyticsAgent
**Capabilities:** `analyze_timetable`, `generate_insights`, `recommend_improvements`

**Responsibilities:**
- Analyzes timetable patterns
- Generates actionable insights
- Recommends improvements
- Identifies optimization opportunities

**Methods:**
- `analyze_timetable()` - Statistical analysis
- `generate_insights()` - Identifies issues and patterns
- `recommend_improvements()` - Suggests optimizations

### 8. ChatbotAgent
**Capabilities:** Natural language interface

**Responsibilities:**
- Natural language processing
- Intent detection
- User interaction
- Command interpretation

## Agent Communication Flow

### Timetable Generation Workflow

```
1. Orchestrator → ValidationAgent
   ├─ validate_data()
   ├─ check_completeness()
   └─ verify_constraints()

2. Orchestrator → MonitoringAgent
   └─ track_performance(generation_started)

3. Orchestrator → ResourceAllocationAgent
   └─ allocate_rooms()

4. Orchestrator → OptimizationAgent
   └─ optimize_timetable()

5. Orchestrator → ConstraintAgent
   └─ validate_constraints()

6. If conflicts → ConflictResolutionAgent
   └─ resolve_conflicts()

7. Orchestrator → OptimizationAgent
   └─ calculate_utilization()

8. Orchestrator → ResourceAllocationAgent
   └─ optimize_floor_allocation()

9. Orchestrator → AnalyticsAgent
   ├─ analyze_timetable()
   ├─ generate_insights()
   └─ recommend_improvements()

10. Orchestrator → MonitoringAgent
    └─ track_performance(generation_completed)
```

## MCP Integration

### Message Format
```json
{
  "id": "unique-message-id",
  "method": "method_name",
  "params": {
    "key": "value"
  },
  "sender": "AgentName",
  "receiver": "TargetAgent",
  "timestamp": 1234567890.123
}
```

### Agent Registration
```python
# Agents register with MCP server
await mcp_client.connect()
await mcp_client.send_message(
    receiver="TargetAgent",
    method="process_request",
    params={"data": "value"}
)
```

## A2A Communication

### Direct Agent-to-Agent
```python
# Orchestrator sends message to agent
result = await orchestrator.send_agent_message(
    sender="Orchestrator",
    receiver_agent=validation_agent,
    method="validate_data",
    params=input_data
)
```

### Message Logging
All A2A messages are logged in the Agent Registry:
- Sender/Receiver
- Method called
- Status (sent/completed/failed)
- Timestamp
- Data payload

## Agent Registry

### Features
- **Service Discovery**: Find agents by capability
- **Health Monitoring**: Track agent status
- **Message Logging**: Complete audit trail
- **Metrics**: Message counts, performance stats

### API
```python
registry = AgentRegistry()

# Register agent
registry.register_agent("AgentName", ["capability1", "capability2"])

# Find agents by capability
agents = registry.find_agent_by_capability("validate_data")

# Log message
registry.log_message("Sender", "Receiver", "method", "status")

# Get message log
logs = registry.get_message_log(limit=100)
```

## Configuration

### Enable MCP
```python
# In orchestrator initialization
orchestrator = AgentOrchestrator(mcp_enabled=True)
await orchestrator.initialize()
```

### MCP Server
```python
# Start MCP server
from mcp_server.enhanced_server import EnhancedMCPServer

server = EnhancedMCPServer(host="localhost", port=8765)
await server.start()
```

## API Response Format

### Success Response
```json
{
  "status": "success",
  "timetable": [...],
  "constraints": [...],
  "utilization": {...},
  "analytics": {...},
  "insights": [...],
  "recommendations": [...],
  "generation_time": 2.45,
  "message_log": [...],
  "agent_status": {...}
}
```

### Enhanced Features
- **message_log**: Complete A2A communication log
- **agent_status**: Status of all agents
- **analytics**: Statistical analysis
- **insights**: Identified issues and patterns
- **recommendations**: Improvement suggestions

## Running the System

### 1. Start MCP Server (Optional)
```bash
python mcp_server/enhanced_server.py
```

### 2. Start Backend
```bash
cd backend
python main.py
```

### 3. Start Frontend
```bash
cd frontend
npm run dev
```

## Testing Agents

```python
# Test individual agent
from agents import ValidationAgent

agent = ValidationAgent()
await agent.initialize()

result = await agent.process_request({
    'method': 'validate_data',
    'params': input_data
})
```

## Benefits

### 1. Modularity
- Each agent has single responsibility
- Easy to add/remove agents
- Independent testing

### 2. Scalability
- Agents can run on different machines
- MCP enables distributed architecture
- Load balancing possible

### 3. Observability
- Complete message logging
- Performance tracking
- Health monitoring

### 4. Flexibility
- MCP can be enabled/disabled
- Fallback to direct calls
- Graceful degradation

### 5. Intelligence
- Validation before generation
- Real-time monitoring
- Analytics and insights
- Continuous improvement recommendations

## Future Enhancements

1. **Machine Learning Agent**: Learn from past timetables
2. **Prediction Agent**: Predict generation success probability
3. **Notification Agent**: Alert on issues
4. **Caching Agent**: Cache common patterns
5. **Load Balancer**: Distribute work across agent instances
