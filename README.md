# University Timetable Management System

An intelligent multi-agent AI system that automates university timetable generation using constraint programming, MCP protocol, and modern web technologies.

## Features

- Multi-agent AI system with 4 specialized agents
- Natural language chatbot interface
- Multi-step workflow with review and verification
- Constraint-based scheduling using Google OR-Tools
- Real-time agent communication logging
- Export and approval functionality
- Modern responsive UI

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
├── agents/              # AI agents
│   ├── constraint_agent.py
│   ├── optimization_agent.py
│   ├── conflict_resolution_agent.py
│   ├── resource_allocation_agent.py
│   ├── orchestrator.py
│   └── chatbot_agent.py
├── backend/             # FastAPI server
│   ├── main.py
│   ├── seed_data.py
│   └── requirements.txt
├── database/            # Database models
│   ├── models.py
│   └── database.py
├── frontend/            # React application
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── components/
│   ├── package.json
│   └── vite.config.js
├── mcp_server/          # MCP protocol (optional)
└── config/              # Configuration
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

Test the agent system:
```bash
cd agents
python test_agents.py
```

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
