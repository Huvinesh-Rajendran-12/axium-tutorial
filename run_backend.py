#!/usr/bin/env python3
"""
Run the Smart Recipe Analyzer backend server.
Supports command-line arguments for configuration.
"""

import os
import sys
import argparse
import uvicorn


def main():
    parser = argparse.ArgumentParser(description="Smart Recipe Analyzer Backend Server")
    
    # Server configuration
    parser.add_argument(
        "--host", 
        default="0.0.0.0", 
        help="Host to bind the server to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000, 
        help="Port to bind the server to (default: 8000)"
    )
    parser.add_argument(
        "--debug", 
        action="store_true", 
        help="Enable debug mode with auto-reload"
    )
    
    # Mode configuration
    parser.add_argument(
        "--agentic", 
        action="store_true", 
        help="Enable agentic mode with tools (default: non-agentic)"
    )
    
    args = parser.parse_args()
    
    # Set environment variables based on arguments
    if args.debug:
        os.environ["DEBUG"] = "True"
    
    if args.agentic:
        os.environ["AGENTIC_MODE"] = "True"
        print("🤖 Starting in AGENTIC mode with tools...")
    else:
        print("🧠 Starting in STANDARD mode...")
    
    # Import after setting environment variables
    from backend.config import HOST, PORT, DEBUG
    
    # Use command line args if provided, otherwise fall back to config
    host = args.host if args.host != "0.0.0.0" else HOST
    port = args.port if args.port != 8000 else PORT
    debug = args.debug or DEBUG
    
    print(f"Starting server at http://{host}:{port}")
    if debug:
        print("Debug mode enabled - server will auto-reload on changes")
    
    # Run the server
    uvicorn.run(
        "backend.app:app",
        host=host,
        port=port,
        reload=debug,
        log_level="debug" if debug else "info"
    )


if __name__ == "__main__":
    main()