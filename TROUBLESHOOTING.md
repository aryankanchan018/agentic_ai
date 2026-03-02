# Troubleshooting Guide

## Common Issues and Solutions

### 1. Backend Won't Start

#### Issue: "Module not found"
```bash
# Solution: Install dependencies
cd backend
pip install -r requirements.txt
```

#### Issue: "Port 8000 already in use"
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F

# Or change port in backend/main.py
uvicorn.run(app, host="0.0.0.0", port=8001)
```

#### Issue: "Database error"
```bash
# Delete and recreate database
cd backend
rm timetable.db
python seed_data.py
```

### 2. Frontend Won't Start

#### Issue: "npm not found"
```
Download and install Node.js from:
https://nodejs.org/
```

#### Issue: "Port 5173 already in use"
```powershell
# Find and kill process
netstat -ano | findstr :5173
taskkill /PID <PID> /F
```

#### Issue: "Module not found" or "Dependencies error"
```bash
cd frontend
rm -r node_modules
rm package-lock.json
npm install
```

### 3. Application Issues

#### Issue: "Blank page in browser"
1. Check browser console (F12)
2. Verify backend is running on port 8000
3. Check network tab for API errors
4. Clear browser cache

#### Issue: "CORS error"
1. Ensure backend is running
2. Check CORS settings in backend/main.py
3. Verify frontend is accessing correct API URL

#### Issue: "Cannot generate timetable"
1. Ensure all data categories have entries
2. Check timeslots are seeded
3. Review constraint violations in output
4. Check backend logs for errors

### 4. Database Issues

#### Issue: "Database is locked"
```bash
# Close all terminals
# Delete database
rm backend/timetable.db
# Reinitialize
python backend/seed_data.py
```

#### Issue: "No timeslots found"
```bash
cd backend
python seed_data.py
```

### 5. Chatbot Issues

#### Issue: "Chatbot not responding"
1. Check backend is running
2. Verify /chat/ endpoint in API docs
3. Check browser console for errors
4. Ensure chatbot_agent.py exists

#### Issue: "Suggestions not working"
1. Check /chat/suggestions/ endpoint
2. Verify backend logs
3. Test endpoint in API docs

### 6. Installation Issues

#### Issue: "pip install fails"
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install packages one by one
pip install fastapi
pip install uvicorn
pip install sqlalchemy
pip install ortools
```

#### Issue: "npm install fails"
```bash
# Clear npm cache
npm cache clean --force

# Try with legacy peer deps
npm install --legacy-peer-deps
```

### 7. Performance Issues

#### Issue: "Slow timetable generation"
1. Reduce solver timeout in config/config.py
2. Limit number of divisions/subjects
3. Check system resources

#### Issue: "Frontend slow to load"
1. Clear browser cache
2. Check network tab for large files
3. Run production build: npm run build

### 8. Git Issues

#### Issue: "Merge conflicts"
```bash
# Stash your changes
git stash

# Pull latest
git pull origin main

# Apply your changes
git stash pop
```

#### Issue: "Cannot push to GitHub"
```bash
# Check remote
git remote -v

# Set remote if needed
git remote add origin <your-repo-url>

# Force push (use carefully)
git push -f origin main
```

### 9. Environment Issues

#### Issue: "Python version mismatch"
```bash
# Check Python version
python --version

# Use specific Python version
python3.10 -m venv venv
```

#### Issue: "Node version mismatch"
```bash
# Check Node version
node --version

# Use nvm to switch versions (if installed)
nvm use 18
```

### 10. Testing Issues

#### Issue: "Tests fail"
```bash
cd agents
python test_agents.py

# If errors, check:
# 1. All dependencies installed
# 2. Database initialized
# 3. Correct Python path
```

## Getting Help

If issues persist:

1. Check API documentation: http://localhost:8000/docs
2. Review backend logs in terminal
3. Check browser console (F12)
4. Verify all prerequisites are installed
5. Try clean reinstall:
   ```bash
   # Backend
   cd backend
   rm -r __pycache__
   pip install -r requirements.txt
   
   # Frontend
   cd frontend
   rm -r node_modules
   npm install
   ```

## Logs Location

- Backend logs: Terminal where `python main.py` is running
- Frontend logs: Browser console (F12)
- Database: `backend/timetable.db`

## Reset Everything

If all else fails, complete reset:

```bash
# Delete database
rm backend/timetable.db

# Delete Python cache
rm -r backend/__pycache__
rm -r agents/__pycache__
rm -r database/__pycache__

# Delete frontend build
rm -r frontend/node_modules
rm -r frontend/dist

# Reinstall
cd backend
pip install -r requirements.txt
python seed_data.py

cd ../frontend
npm install

# Restart servers
cd ../backend
python main.py

# New terminal
cd frontend
npm run dev
```
