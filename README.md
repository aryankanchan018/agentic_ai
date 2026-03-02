# University Timetable Management System

An intelligent multi-agent AI system that automates university timetable generation using constraint programming, MCP protocol, and modern web technologies.

## Overview

Universities face significant challenges in creating conflict-free timetables due to multiple classes, divisions, labs, limited rooms across different floors, faculty availability constraints, student group scheduling, lab vs classroom requirements, and capacity limitations.

This system solves these problems using Agentic AI with 4 specialized AI agents working collaboratively, MCP (Model Context Protocol) for standardized agent communication, A2A (Agent-to-Agent) coordination for intelligent problem-solving, constraint programming using Google OR-Tools, and a modern web UI.

## Key Features

### Multi-Agent System
- Constraint Agent: Validates scheduling rules and prevents conflicts
- Optimization Agent: Uses OR-Tools CP-SAT solver for optimal scheduling
- Conflict Resolution Agent: Intelligently resolves scheduling conflicts
- Resource Allocation Agent: Manages rooms, labs, floors, and benches

### Intelligent Scheduling
- Prevents faculty double-booking
- Avoids room conflicts
- Ensures students aren't in two places at once
- Matches lab subjects with lab rooms
- Respects room capacity and bench counts
- Optimizes floor allocation to minimize movement
- Minimizes gaps in daily schedules

### Modern Web Interface
- Clean gradient UI with smooth animations
- Tabbed data input for departments, subjects, rooms, faculty, divisions
- Real-time validation and feedback
- Interactive timetable visualization
- Agent communication logs (A2A transparency)
- Responsive design

## Architecture

```
React Frontend (Modern UI with Tabbed Interface)
    |
    | REST API
    v
FastAPI Backend (API Endpoints & Orchestration)
    |
    v
Agent Orchestrator (Coordinates Multi-Agent Workflow)
    |
    +-- Constraint Agent
    +-- Optimization Agent
    +-- Conflict Resolution Agent
    +-- Resource Allocation Agent
    |
    v
SQLite Database (Departments, Subjects, Rooms, Faculty, Divisions)
```

## Quick Start

### Prerequisites
- Python 3.10 or higher
- Node.js 18 or higher
- pip and npm

### Installation

**Backend Setup**
```bash
cd backend
pip install -r requirements.txt
python seed_data.py
python main.py
```
Backend runs on http://localhost:8000

**Frontend Setup (New Terminal)**
```bash
cd frontend
npm install
npm run dev
```
Frontend runs on http://localhost:5173

## Usage Guide

1. Access the application at http://localhost:5173
2. Use the tabbed interface to add your data:
   - Departments: Name and Code
   - Subjects: Name, Code, Hours per week, Lab flag
   - Rooms: Room number, Floor, Capacity, Bench count, Lab flag
   - Faculty: Name and Employee ID
   - Divisions: Name, Year, Student count
3. Click "Generate Timetable" button
4. Review the generated timetable with metrics and agent logs

## Technology Stack

### Backend
- FastAPI: High-performance Python web framework
- SQLAlchemy: SQL toolkit and ORM
- OR-Tools: Google's constraint programming solver
- Pydantic: Data validation
- SQLite: Lightweight database

### Frontend
- React 18: Modern UI library
- Vite: Next-generation build tool
- CSS3: Gradients, animations, responsive design

### AI & Agents
- Custom Multi-Agent System
- MCP Protocol: WebSocket-based agent communication
- Constraint Programming: OR-Tools CP-SAT solver

## Project Structure

```
agentic_ai/
├── agents/
│   ├── constraint_agent.py
│   ├── optimization_agent.py
│   ├── conflict_resolution_agent.py
│   ├── resource_allocation_agent.py
│   ├── orchestrator.py
│   └── test_agents.py
├── backend/
│   ├── main.py
│   ├── seed_data.py
│   └── requirements.txt
├── database/
│   ├── models.py
│   └── database.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── components/
│   │       ├── DataInput.jsx
│   │       └── TimetableView.jsx
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── mcp_server/
│   ├── server.py
│   └── client.py
├── config/
│   └── config.py
├── .gitignore
├── .env.example
└── README.md
```

## Testing

Test the agent system:
```bash
cd agents
python test_agents.py
```

API documentation available at: http://localhost:8000/docs

## Configuration

Edit `config/config.py` to customize:
- Maximum hours per day
- Working days
- Lunch break slot
- Solver timeout
- Constraint parameters

## How It Works

### Agent Workflow

1. User Input: Frontend collects university data
2. Data Validation: Backend validates and stores data
3. Resource Allocation Agent: Matches rooms to requirements
4. Optimization Agent: Generates optimal schedule using OR-Tools
5. Constraint Agent: Validates all constraints
6. Conflict Resolution Agent: Resolves any conflicts
7. Results: Display timetable with metrics and logs

### A2A Communication
All agents communicate through the orchestrator, logging every interaction for transparency.

## API Endpoints

### Data Management
- POST /departments/ - Create department
- GET /departments/ - List all departments
- POST /subjects/ - Create subject
- GET /subjects/ - List all subjects
- POST /rooms/ - Create room
- GET /rooms/ - List all rooms
- POST /faculty/ - Create faculty
- GET /faculty/ - List all faculty
- POST /divisions/ - Create division
- GET /divisions/ - List all divisions

### Timetable Generation
- POST /generate-timetable/ - Generate timetable

## Troubleshooting

**Backend won't start**
- Ensure Python 3.10+ is installed
- Check if port 8000 is available
- Verify all dependencies are installed

**Frontend won't start**
- Ensure Node.js 18+ is installed
- Check if port 5173 is available
- Try deleting node_modules and running npm install again

**No timetable generated**
- Ensure all data categories have at least one entry
- Check constraint violations in the output
- Verify timeslots are seeded

## License

MIT License

## Contributing

Contributions are welcome. Please submit a Pull Request.

## Acknowledgments

- Google OR-Tools for constraint programming
- FastAPI for the web framework
- React team for the UI library
