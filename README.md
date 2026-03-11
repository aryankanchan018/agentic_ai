# University Timetable Management System

An intelligent **multi-agent AI system** that automates university timetable generation using **MCP (Model Context Protocol)**, **A2A (Agent-to-Agent) communication**, constraint programming, and modern web technologies.

## Features

- **8 Specialized AI Agents** with distinct responsibilities
- **MCP Protocol** for standardized agent communication
- **A2A Messaging** for distributed coordination
- **Agent Registry** for service discovery and monitoring
- **Real-time Analytics** and insights
- **Performance Monitoring** and health checks
- Natural language chatbot interface
- Constraint-based scheduling using Google OR-Tools
- Modern responsive UI

## Multi-Agent Architecture

### Agents

1. **ValidationAgent** - Pre-flight data validation
2. **ResourceAllocationAgent** - Room and resource management
3. **OptimizationAgent** - Constraint programming solver
4. **ConstraintAgent** - Constraint validation
5. **ConflictResolutionAgent** - Conflict resolution strategies
6. **MonitoringAgent** - Performance tracking and health monitoring
7. **AnalyticsAgent** - Insights and recommendations
8. **ChatbotAgent** - Natural language interface

### Communication Flow

```
Orchestrator → ValidationAgent → ResourceAllocationAgent → 
OptimizationAgent → ConstraintAgent → ConflictResolutionAgent → 
AnalyticsAgent → MonitoringAgent
```

All communication is logged via **Agent Registry** for complete observability.

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed documentation.

## Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- pip and npm

## Quick Start

### Automated Setup (Recommended)

Run the setup script:

```powershell
.\setup.ps1
```

This will:
1. Check prerequisites
2. Install all dependencies
3. Initialize database
4. Start backend and frontend servers

### Manual Setup

#### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python seed_data.py
python main.py
```

Backend runs on http://localhost:8000

#### Frontend Setup (New Terminal)

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on http://localhost:5173

## Usage

1. Open http://localhost:5173 in your browser
2. Add university data using the tabbed interface or chatbot
3. Review and verify your data
4. Generate timetable
5. View results with metrics and agent logs

### Using the Chatbot

Click the chat button (💬) in the bottom-right corner and try:
- "Add a new department"
- "Generate timetable"
- "Show all subjects"
- "Help"

## Project Structure

```
agentic_ai/
├── agents/                    # AI Agents (8 specialized agents)
│   ├── base_agent.py         # Base agent class with MCP support
│   ├── agent_registry.py     # Service discovery and logging
│   ├── validation_agent.py   # Data validation
│   ├── resource_allocation_agent.py  # Resource management
│   ├── optimization_agent.py # Constraint solver
│   ├── constraint_agent.py   # Constraint validation
│   ├── conflict_resolution_agent.py  # Conflict resolution
│   ├── monitoring_agent.py   # Performance monitoring
│   ├── analytics_agent.py    # Insights and recommendations
│   ├── chatbot_agent.py      # Natural language interface
│   ├── orchestrator.py       # Agent coordination
│   └── test_enhanced_agents.py  # Comprehensive tests
├── backend/                   # FastAPI server
│   ├── main.py
│   ├── seed_data.py
│   └── requirements.txt
├── database/                  # Database models
│   ├── models.py
│   └── database.py
├── frontend/                  # React application
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── components/
│   ├── package.json
│   └── vite.config.js
├── mcp_server/                # MCP protocol implementation
│   ├── server.py             # Basic MCP server
│   ├── enhanced_server.py    # Enhanced MCP with registry
│   └── client.py             # MCP client
├── config/                    # Configuration
│   └── config.py
├── ARCHITECTURE.md            # Detailed architecture docs
└── README.md
```

## Technology Stack

### Backend
- FastAPI - Web framework
- SQLAlchemy - ORM
- OR-Tools - Constraint solver
- Pydantic - Data validation
- SQLite - Database

### Frontend
- React 18 - UI library
- Vite - Build tool
- CSS3 - Styling

### AI & Agents
- Custom multi-agent system
- MCP protocol
- Natural language processing
- Constraint programming

## API Documentation

Once backend is running, visit:
http://localhost:8000/docs

## Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Module not found:**
```bash
pip install -r requirements.txt
```

### Frontend Issues

**Port 5173 already in use:**
```powershell
netstat -ano | findstr :5173
taskkill /PID <PID> /F
```

**Dependencies error:**
```bash
rm -r node_modules
npm install
```

### Database Issues

**Database locked:**
```bash
# Delete database and reinitialize
rm backend/timetable.db
python backend/seed_data.py
```

## Configuration

Edit `config/config.py` to customize:
- Maximum hours per day
- Working days
- Solver timeout
- Constraint parameters

## Testing

Test the enhanced multi-agent system:
```bash
cd agents
python test_enhanced_agents.py
```

This will test:
- All 8 agents individually
- Agent Registry
- Full orchestration workflow
- A2A communication
- Performance monitoring
- Analytics and insights

## MCP Server (Optional)

To enable MCP-based agent communication:

```bash
# Terminal 1: Start MCP Server
python mcp_server/enhanced_server.py

# Terminal 2: Start Backend with MCP enabled
# Agents will automatically connect to MCP server
python backend/main.py
```

## Agent Communication

The system supports two modes:

1. **Direct Mode** (Default): Agents communicate via direct function calls
2. **MCP Mode**: Agents communicate via WebSocket-based MCP protocol

Both modes provide complete message logging and observability.

## Features by Branch

- `main` - Stable version with all features
- `feature/enhanced-ui` - Multi-step workflow
- `feature/chatbot-interface` - Natural language chatbot

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License

## Acknowledgments

- Google OR-Tools for constraint programming
- FastAPI for the web framework
- React team for the UI library
