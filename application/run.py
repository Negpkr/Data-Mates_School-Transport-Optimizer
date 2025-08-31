#!/usr/bin/env python3
"""
Trust Track - Startup Script
A simple script to run the Trust Track school safety demo application.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    print(f"Python version: {sys.version.split()[0]}")
    return True

def check_data_files():
    """Check if required data files exist."""
    data_dir = Path("data")
    required_files = [
        "ACT_School_Bus_Services.csv",
        "Park_And_Ride_Locations.csv", 
        "Daily_Public_Transport_Passenger_Journeys_by_Service_Type_20250830.csv"
    ]
    
    missing_files = []
    for file in required_files:
        if not (data_dir / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("Missing required data files:")
        for file in missing_files:
            print(f"   - data/{file}")
        print("\nPlease ensure all CSV files are in the data/ directory.")
        return False
    
    print("All required data files found")
    return True

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import fastapi
        import uvicorn
        import osmnx
        import networkx
        import pandas
        import numpy
        import shapely
        import folium
        print("All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("\nPlease install dependencies with:")
        print("pip install -r requirements.txt")
        return False

def create_virtual_env():
    """Create virtual environment if it doesn't exist."""
    venv_path = Path(".venv")
    if not venv_path.exists():
        print("Creating virtual environment...")
        try:
            subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
            print("Virtual environment created")
            print("\nPlease activate it and install dependencies:")
            if os.name == 'nt':  # Windows
                print(".venv\\Scripts\\activate")
            else:  # Unix/Linux/macOS
                print("source .venv/bin/activate")
            print("pip install -r requirements.txt")
            return False
        except subprocess.CalledProcessError:
            print("Failed to create virtual environment")
            return False
    return True

def main():
    """Main startup function."""
    print("Trust Track - School Safety Demo")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check if we're in a virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("Not running in a virtual environment")
        if not create_virtual_env():
            sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check data files
    if not check_data_files():
        sys.exit(1)
    
    print("\nStarting Trust Track application...")
    print("Open your browser to: http://localhost:8000")
    print("API documentation: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Import and run the app
        from app import app
        import uvicorn
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info",
            reload=True
        )
    except KeyboardInterrupt:
        print("\nTrust Track stopped")
    except Exception as e:
        print(f"\nError starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
