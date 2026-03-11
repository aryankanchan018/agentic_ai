# Quick Start Guide - Enhanced Multi-Agent System

## What's New

Your timetable system now has:
- **8 specialized agents** (was 4)
- **MCP protocol** for agent communication
- **Agent Registry** for service discovery
- **Real-time monitoring** and analytics
- **Insights and recommendations**
- **Complete A2A message logging**

## New Agents

### 1. ValidationAgent
Validates all input data before timetable generation starts.

### 2. MonitoringAgent
Tracks performance metrics, success rates, and system health.

### 3. AnalyticsAgent
Analyzes generated timetables and provides insights and recommendations.

## Quick Test

### Test Individual Agents
```bash
cd agents
python test_enhanced_agents.py
```

Expected output:
```
=== Testing ValidationAgent ===
Validation Result: valid
✓ ValidationAgent tests passed

=== Testing MonitoringAgent ===
System Health: healthy
✓ MonitoringAgent tests passed

=== Testing AnalyticsAgent ===
Statistics: {...}
Insights: 3 found
Recommendations: 2 generated
✓ AnalyticsAgent tests passed

=== Testing AgentOrchestrator (Full Workflow) ===
Starting timetable generation...
[Orchestrator] Step 1: Validating input data...
[Orchestrator] Step 2: Checking data completeness...
[Orchestrator] Step 3: Allocating rooms...
[Orchestrator] Step 4: Generating optimal timetable...
[Orchestrator] Step 5: Validating constraints...
[Orchestrator] Step 7: Calculating utilization metrics...
[Orchestrator] Step 8: Generating analytics insights...
[Orchestrator] Timetable generation completed in 2.45s

Generation Status: success
Generation Time: 2.45s
Timetable Entries: 18
Insights Generated: 3
Recommendations: 2
Message Log Entries: 15

ALL TESTS PASSED ✓
```

## Enhanced API Response

The `/api/generate-timetable/` endpoint now returns:

```json
{
  "status": "success",
  "timetable": [...],
  "constraints": [...],
  "utilization": {
    "slot_utilization": 0.75,
    "room_utilization": {...},
    "average_room_usage": 6.5
  },
  "analytics": {
    "total_classes": 18,
    "room_balance_score": 85,
    "faculty_balance_score": 90
  },
  "insights": [
    {
      "type": "schedule_gap",
      "severity": "medium",
      "message": "Division 1 has 2 gap(s) on Monday"
    }
  ],
  "recommendations": [
    {
      "category": "workload_balancing",
      "priority": "high",
      "recommendation": "Redistribute teaching load more evenly"
    }
  ],
  "generation_time": 2.45,
  "message_log": [...],
  "agent_status": {
    "ValidationAgent": {
      "status": "active",
      "message_count": 3
    },
    "OptimizationAgent": {
      "status": "active",
      "message_count": 2
    }
  }
}
```

## Using MCP (Optional)

### Start MCP Server
```bash
python mcp_server/enhanced_server.py
```

Output:
```
[MCP Server] Running on ws://localhost:8765
```

### Enable MCP in Code
```python
from agents import AgentOrchestrator

# Create orchestrator with MCP enabled
orchestrator = AgentOrchestrator(mcp_enabled=True)

# Initialize (connects agents to MCP server)
await orchestrator.initialize()

# Generate timetable
result = orchestrator.generate_timetable(input_data)
```

## Agent Registry API

### Check Agent Status
```python
from agents import AgentRegistry

registry = AgentRegistry()

# Get all agents
agents = registry.get_all_agents()

# Find agents by capability
validation_agents = registry.find_agent_by_capability('validate_data')

# Get message log
messages = registry.get_message_log(limit=50)
```

## Monitoring Dashboard (Future)

The MonitoringAgent tracks:
- Total timetable generations
- Success/failure rates
- Average generation time
- Constraint violations
- Conflicts resolved

Access via:
```python
monitoring_agent = MonitoringAgent()
report = await monitoring_agent.process_request({
    'method': 'generate_report',
    'params': {}
})
print(report['summary'])
```

## Analytics Insights

The AnalyticsAgent provides:

1. **Schedule Gaps**: Identifies gaps in division schedules
2. **Room Utilization**: Detects under/over-utilized rooms
3. **Faculty Load**: Identifies overloaded faculty
4. **Balance Scores**: Room and faculty distribution metrics

## Recommendations

The system now suggests improvements:
- Resource balancing
- Workload distribution
- Schedule optimization
- Consecutive class reduction

## Architecture Benefits

### 1. Modularity
Each agent has a single, well-defined responsibility.

### 2. Observability
Complete message logging shows exactly what each agent did.

### 3. Scalability
Agents can be distributed across machines using MCP.

### 4. Intelligence
Validation, monitoring, and analytics provide continuous improvement.

### 5. Flexibility
MCP can be enabled/disabled without code changes.

## Next Steps

1. **Run tests**: `python agents/test_enhanced_agents.py`
2. **Start backend**: `python backend/main.py`
3. **Start frontend**: `cd frontend && npm run dev`
4. **Generate timetable**: Use the UI or API
5. **Review insights**: Check the analytics and recommendations

## Troubleshooting

### Agents not initializing
- Check if all agent files are present
- Verify Python path includes parent directory

### MCP connection failed
- Ensure MCP server is running
- Check port 8765 is not in use
- System falls back to direct mode automatically

### Import errors
- Run: `pip install -r backend/requirements.txt`
- Ensure you're in the correct directory

## Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - Detailed architecture
- [README.md](README.md) - Main documentation
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues

## Support

For issues or questions:
1. Check ARCHITECTURE.md for detailed explanations
2. Run test suite to verify setup
3. Review message logs for debugging
