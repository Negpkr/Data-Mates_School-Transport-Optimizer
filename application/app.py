#!/usr/bin/env python3
"""
Trust Track - School Safety Demo Application
A FastAPI application providing school safety routing with a modern frontend.
"""

import os
import sys
from pathlib import Path
from datetime import date
from typing import Optional, Dict, Any, List

import uvicorn
from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from trusttrack.api import app as api_app
from trusttrack.utils import build_graph_bbox, find_data, parse_wkt_point_lonlat_to_latlon, parse_paren_latlon
from trusttrack.routing import compute_walk_routes, compute_bus_options, apply_bus_safety_and_pick_safest, compute_pr_options, make_geojson

# Create the main FastAPI app
app = FastAPI(
    title="Trust Track - School Safety",
    description="A school safety routing application for parents and students",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

# Mount static files (frontend)
frontend_path = project_root / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

# Data models
class RouteRequest(BaseModel):
    origin: str
    school: Optional[str] = None
    dest: Optional[str] = None
    date_str: Optional[str] = None
    time_str: Optional[str] = None

class RouteResponse(BaseModel):
    origin: Dict[str, Any]
    destination: Dict[str, Any]
    walk: Dict[str, Any]
    bus: Dict[str, Any]
    park_and_ride: List[Dict[str, Any]]
    links: Dict[str, Any]
    geojson: Dict[str, Any]

# Load data files
DATA_FILES = {
    "school_bus": "ACT_School_Bus_Services.csv",
    "park_ride": "Park_And_Ride_Locations.csv",
    "journeys": "Daily_Public_Transport_Passenger_Journeys_by_Service_Type_20250830.csv",
}

# Load CSVs once at startup
try:
    import pandas as pd
    
    bus_df = pd.read_csv(find_data(DATA_FILES["school_bus"]))
    assert "Location" in bus_df.columns, "School Bus CSV must have 'Location' (WKT POINT)"
    bus_df["lat"], bus_df["lon"] = zip(*bus_df["Location"].map(parse_wkt_point_lonlat_to_latlon))
    bus_df = bus_df.dropna(subset=["lat","lon"]).copy()

    pr_df = pd.read_csv(find_data(DATA_FILES["park_ride"]))
    assert "Point" in pr_df.columns, "Park & Ride CSV must have 'Point' like '(-35.2, 149.1)'"
    pr_df["lat"], pr_df["lon"] = zip(*pr_df["Point"].map(parse_paren_latlon))
    pr_df = pr_df.dropna(subset=["lat","lon"]).copy()

    dj_df = pd.read_csv(find_data(DATA_FILES["journeys"]))
    
    print("Data files loaded successfully")
except Exception as e:
    print(f"Error loading data files: {e}")
    bus_df = pr_df = dj_df = None

# Available schools (from the data)
AVAILABLE_SCHOOLS = [
    "Ainslie School",
    "Lyneham High School", 
    "Canberra High School",
    "Dickson College",
    "Telopea Park School",
    "Narrabundah College",
    "Melrose High School",
    "Alfred Deakin High School",
    "Garran Primary School",
    "Red Hill Primary School"
]

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the main frontend application."""
    frontend_file = frontend_path / "index.html"
    if frontend_file.exists():
        return FileResponse(frontend_file)
    else:
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Trust Track - School Safety</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                .error { color: #dc2626; }
            </style>
        </head>
        <body>
            <h1>🛡️ Trust Track</h1>
            <p class="error">Frontend files not found. Please ensure the frontend directory exists.</p>
            <p>API is available at <a href="/docs">/docs</a></p>
        </body>
        </html>
        """

@app.get("/api/schools")
async def get_schools():
    """Get list of available schools."""
    return {"schools": AVAILABLE_SCHOOLS}

@app.get("/api/route")
async def api_route(
    origin: str = Query(..., description="lat,lon coordinates"),
    school: Optional[str] = Query(None, description="School name"),
    dest: Optional[str] = Query(None, description="lat,lon destination (optional)"),
    date_str: Optional[str] = Query(None, description="YYYY-MM-DD date"),
    time_str: Optional[str] = Query(None, description="HH:MM time")
) -> Dict[str, Any]:
    """
    Plan a route from origin to school or destination.
    
    Args:
        origin: Starting point coordinates (lat,lon)
        school: School name (if dest not provided)
        dest: Destination coordinates (lat,lon) - optional
        date_str: Date for the journey (YYYY-MM-DD)
        time_str: Departure time (HH:MM)
    
    Returns:
        Route information including walking, bus, and park & ride options
    """
    
    # Validate data is loaded
    if bus_df is None or pr_df is None or dj_df is None:
        raise HTTPException(500, "Data files not loaded. Please check server configuration.")
    
    # Parse origin coordinates
    try:
        olat, olon = [float(x.strip()) for x in origin.split(",")]
    except Exception:
        raise HTTPException(400, "origin must be 'lat,lon' format")
    
    # Determine destination
    if dest:
        try:
            dlat, dlon = [float(x.strip()) for x in dest.split(",")]
        except Exception:
            raise HTTPException(400, "dest must be 'lat,lon' format")
        school_name = None
    elif school:
        try:
            import osmnx as ox
            dlat, dlon = ox.geocoder.geocode(f"{school}, Australian Capital Territory, Australia")
        except Exception as e:
            raise HTTPException(400, f"Geocoding failed for school '{school}': {e}")
        school_name = school
    else:
        raise HTTPException(400, "Provide either 'dest' coordinates or 'school' name")
    
    origin_ll = (olat, olon)
    dest_ll = (dlat, dlon)
    
    try:
        # Build graph for this origin-destination pair
        G = build_graph_bbox(origin_ll, dest_ll, buffer_km=6.0)
        
        # Compute walking routes
        walk = compute_walk_routes(G, origin_ll, dest_ll)
        
        # Compute bus options
        bus = compute_bus_options(G, origin_ll, dest_ll, bus_df, school_name)
        
        # Apply safety factors and pick safest bus option
        target_date = date.fromisoformat(date_str) if date_str else date.today()
        safest = apply_bus_safety_and_pick_safest(bus["options_df"], dj_df, target_date)
        
        # Compute park & ride options
        pr_top = compute_pr_options(G, dest_ll, pr_df)
        
        # Generate Google Maps links
        def gmaps_dir(origin_ll, dest_ll, mode="walking"):
            return (
                "https://www.google.com/maps/dir/?api=1"
                f"&origin={origin_ll[0]},{origin_ll[1]}"
                f"&destination={dest_ll[0]},{dest_ll[1]}"
                f"&travelmode={mode}"
            )
        
        walk_link = gmaps_dir(origin_ll, dest_ll, "walking")
        transit_link = gmaps_dir(origin_ll, dest_ll, "transit")
        
        # Generate GeoJSON for map display
        geo = make_geojson(origin_ll, dest_ll, walk, bus["fastest"], safest, pr_top)
        
        return {
            "origin": {"lat": olat, "lon": olon},
            "destination": {"lat": dlat, "lon": dlon, "name": school_name},
            "walk": walk,
            "bus": {
                "fastest": bus["fastest"],
                "safest": safest
            },
            "park_and_ride": pr_top,
            "links": {
                "google": {
                    "walking": walk_link,
                    "transit": transit_link
                }
            },
            "geojson": geo,
        }
        
    except Exception as e:
        raise HTTPException(500, f"Route computation failed: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "data_loaded": all([bus_df is not None, pr_df is not None, dj_df is not None]),
        "available_schools": len(AVAILABLE_SCHOOLS)
    }

@app.get("/api/stats")
async def get_stats():
    """Get application statistics."""
    return {
        "total_schools": len(AVAILABLE_SCHOOLS),
        "bus_stops": len(bus_df) if bus_df is not None else 0,
        "park_ride_locations": len(pr_df) if pr_df is not None else 0,
        "journey_data_points": len(dj_df) if dj_df is not None else 0
    }

# Include the original API routes
app.mount("/api/v1", api_app)

if __name__ == "__main__":
    print("🚀 Starting Trust Track School Safety Demo...")
    print(f"📁 Project root: {project_root}")
    print(f"📁 Frontend path: {frontend_path}")
    print(f"✅ Frontend exists: {frontend_path.exists()}")
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
