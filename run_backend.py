#!/usr/bin/env python3
"""
Simple script to run the backend server.
"""
import uvicorn
from backend.config import HOST, PORT, DEBUG

if __name__ == "__main__":
    print(f"Starting Smart Recipe Analyzer API on {HOST}:{PORT}")
    print(f"Debug mode: {DEBUG}")
    print(f"API docs will be available at: http://{HOST}:{PORT}/docs")
    
    uvicorn.run(
        "backend.app:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
        log_level="debug" if DEBUG else "info"
    )