class Config:
    """Application configuration"""
    
    # Database
    DATABASE_URL = "sqlite:///./timetable.db"
    
    # MCP Server
    MCP_HOST = "localhost"
    MCP_PORT = 8765
    
    # Timetable Generation
    MAX_HOURS_PER_DAY = 8
    WORKING_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    LUNCH_BREAK_SLOT = 4  # 12:00-13:00
    
    # Constraints
    MIN_ROOM_CAPACITY_BUFFER = 5  # Extra seats buffer
    MAX_CONSECUTIVE_CLASSES = 3
    
    # Optimization
    SOLVER_TIMEOUT_SECONDS = 30
    
    # Agent Settings
    AGENT_TIMEOUT = 60
    MAX_RETRIES = 3
