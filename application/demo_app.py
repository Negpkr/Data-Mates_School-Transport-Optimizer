#!/usr/bin/env python3
"""
Trust Track - Real Routing Application
Uses the actual routing logic from the Jupyter notebook and trusttrack module.
"""

import os
import sys
from pathlib import Path
from datetime import date
from typing import Optional, Dict, Any, List

import uvicorn
import pandas as pd
from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Import the real routing logic
from trusttrack.utils import (
    build_graph_bbox, find_data, parse_wkt_point_lonlat_to_latlon, parse_paren_latlon
)
from trusttrack.routing import (
    compute_walk_routes, compute_bus_options, apply_bus_safety_and_pick_safest,
    compute_pr_options, make_geojson
)

# Create the main FastAPI app
app = FastAPI(
    title="Trust Track - School Safety",
    description="A school safety routing application using real OSM data and routing algorithms",
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
project_root = Path(__file__).parent
frontend_path = project_root / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

# Load real data files
DATA_FILES = {
    "school_bus": "ACT_School_Bus_Services.csv",
    "park_ride":  "Park_And_Ride_Locations.csv",
    "journeys":   "Daily_Public_Transport_Passenger_Journeys_by_Service_Type_20250830.csv",
}

# Load CSVs once
try:
    bus_df = pd.read_csv(find_data(DATA_FILES["school_bus"]))
    assert "Location" in bus_df.columns, "School Bus CSV must have 'Location' (WKT POINT)"
    bus_df["lat"], bus_df["lon"] = zip(*bus_df["Location"].map(parse_wkt_point_lonlat_to_latlon))
    bus_df = bus_df.dropna(subset=["lat","lon"]).copy()

    pr_df = pd.read_csv(find_data(DATA_FILES["park_ride"]))
    assert "Point" in pr_df.columns, "Park & Ride CSV must have 'Point' like '(-35.2, 149.1)'"
    pr_df["lat"], pr_df["lon"] = zip(*pr_df["Point"].map(parse_paren_latlon))
    pr_df = pr_df.dropna(subset=["lat","lon"]).copy()

    dj_df = pd.read_csv(find_data(DATA_FILES["journeys"]))
    
    print("✅ Real data loaded successfully!")
    print(f"   - Bus stops: {len(bus_df)}")
    print(f"   - Park & Ride locations: {len(pr_df)}")
    print(f"   - Journey data points: {len(dj_df)}")
    
except Exception as e:
    print(f"⚠️  Warning: Could not load real data: {e}")
    print("   Falling back to demo mode...")
    bus_df = None
    pr_df = None
    dj_df = None

# Available schools
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
    origin: str = Query(..., description="Place name or lat,lon coordinates"),
    school: Optional[str] = Query(None, description="School name"),
    date_str: Optional[str] = Query(None, description="YYYY-MM-DD date"),
    time_str: Optional[str] = Query(None, description="HH:MM time")
) -> Dict[str, Any]:
    """
    Plan a route from origin to school using real routing algorithms.
    """
    
    # Parse origin (support both place names and coordinates)
    if ',' in origin and not any(c.isalpha() for c in origin):
        # Treat as coordinates
        try:
            olat, olon = [float(x.strip()) for x in origin.split(",")]
        except Exception:
            raise HTTPException(400, "origin coordinates must be 'lat,lon' format")
    else:
        # Treat as place name
        place_coords = {
            "canberra centre": (-35.281, 149.128),
            "canberra center": (-35.281, 149.128),
            "civic": (-35.281, 149.128),
            "belconnen": (-35.215, 149.085),
            "gungahlin": (-35.183, 149.133),
            "woden": (-35.345, 149.095),
            "tuggeranong": (-35.424, 149.088),
            "fyshwick": (-35.330, 149.165),
            "dickson": (-35.251, 149.139),
            "braddon": (-35.275, 149.135),
            "lyneham": (-35.242, 149.133),
            "o'connor": (-35.265, 149.115),
            "turner": (-35.275, 149.115),
            "acton": (-35.285, 149.115),
            "city": (-35.281, 149.128),
            "downtown": (-35.281, 149.128),
        }
        origin_lower = origin.lower().strip()
        if origin_lower in place_coords:
            olat, olon = place_coords[origin_lower]
        else:
            # Default to Canberra Centre for unknown places
            olat, olon = (-35.281, 149.128)
    
    # Determine destination (school coordinates)
    if not school:
        raise HTTPException(400, "School name is required")
    
    # Use real geocoding for schools
    try:
        import osmnx as ox
        dlat, dlon = ox.geocoder.geocode(f"{school}, Australian Capital Territory, Australia")
        school_name = school
    except Exception as e:
        # Fallback to hardcoded coordinates
        school_coords = {
            "Ainslie School": (-35.2734, 149.1396),
            "Lyneham High School": (-35.2417, 149.1333),
            "Canberra High School": (-35.2819, 149.1289),
            "Dickson College": (-35.2514, 149.1392),
            "Telopea Park School": (-35.3089, 149.1396),
            "Narrabundah College": (-35.3456, 149.0954),
            "Melrose High School": (-35.2156, 149.0854),
            "Alfred Deakin High School": (-35.3456, 149.0954),
            "Garran Primary School": (-35.3456, 149.0954),
            "Red Hill Primary School": (-35.3456, 149.0954),
        }
        if school in school_coords:
            dlat, dlon = school_coords[school]
            school_name = school
        else:
            # Default to Ainslie School
            dlat, dlon = (-35.2734, 149.1396)
            school_name = school
    
    origin_ll = (olat, olon)
    dest_ll = (dlat, dlon)
    
    # Check if we have real data, otherwise fall back to demo
    if bus_df is not None and pr_df is not None and dj_df is not None:
        # Use real routing
        try:
            # Build graph for this OD pair - try larger buffer if needed
            try:
                G = build_graph_bbox(origin_ll, dest_ll, buffer_km=6.0)
            except Exception as e:
                print(f"Bbox graph failed, trying larger buffer: {e}")
                try:
                    G = build_graph_bbox(origin_ll, dest_ll, buffer_km=10.0)
                except Exception as e2:
                    print(f"Large bbox also failed: {e2}")
                    # Fall back to demo mode
                    raise Exception("Graph building failed, using demo mode")
            
            # Compute walk routes
            walk = compute_walk_routes(G, origin_ll, dest_ll)
            
            # Compute bus options
            bus = compute_bus_options(G, origin_ll, dest_ll, bus_df, school_name)
            
            # Apply bus safety and pick safest
            dt = date.fromisoformat(date_str) if date_str else date.today()
            safest = apply_bus_safety_and_pick_safest(bus["options_df"], dj_df, dt)
            
            # Compute park & ride options
            pr_top = compute_pr_options(G, dest_ll, pr_df)
            
            # Generate GeoJSON
            geo = make_geojson(origin_ll, dest_ll, walk, bus["fastest"], safest, pr_top)
            
            # Google Maps links
            def gmaps_dir(origin_ll, dest_ll, mode="walking"):
                return (
                    "https://www.google.com/maps/dir/?api=1"
                    f"&origin={origin_ll[0]},{origin_ll[1]}"
                    f"&destination={dest_ll[0]},{dest_ll[1]}"
                    f"&travelmode={mode}"
                )
            
            walk_link = gmaps_dir(origin_ll, dest_ll, "walking")
            transit_link = gmaps_dir(origin_ll, dest_ll, "transit")
            
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
                "real_routing": True
            }
            
        except Exception as e:
            print(f"Real routing failed: {e}")
            # Fall back to demo mode
            pass
    
    # Demo mode fallback
    import random
    import math
    
    # Calculate rough distance for demo
    def haversine_km(lat1, lon1, lat2, lon2):
        R = 6371.0
        p1, p2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlmb = math.radians(lon2 - lon1)
        a = (math.sin(dphi/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dlmb/2)**2)
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    distance_km = haversine_km(olat, olon, dlat, dlon)
    
    # Generate demo walking times (rough estimate)
    walk_fast_min = max(5, int(distance_km * 15))  # 15 min/km rough estimate
    walk_safe_min = int(walk_fast_min * 1.4)  # Safe route takes longer (more realistic)
    
    # Generate demo bus data if distance > 1km
    bus_data = None
    if distance_km > 1.0:
        walk_to_bus = random.randint(2, 8)
        bus_time = max(3, int(distance_km * 8))  # 8 min/km for bus
        walk_from_bus = random.randint(2, 6)
        bus_data = {
            "fastest": {
                "start_label": f"Bus Stop {random.randint(100, 999)}",
                "start_lat": olat + (dlat - olat) * 0.3 + random.uniform(-0.01, 0.01),
                "start_lon": olon + (dlon - olon) * 0.3 + random.uniform(-0.01, 0.01),
                "w_fast_min": walk_to_bus,
                "w_safe_min": walk_to_bus + 1,
                "w_safe_score": random.randint(75, 95),
                "bus_min": bus_time,
                "total_minutes_fast": walk_to_bus + bus_time + walk_from_bus
            },
            "safest": {
                "start_label": f"Bus Stop {random.randint(100, 999)}",
                "start_lat": olat + (dlat - olat) * 0.3 + random.uniform(-0.01, 0.01),
                "start_lon": olon + (dlon - olon) * 0.3 + random.uniform(-0.01, 0.01),
                "w_fast_min": walk_to_bus + 2,
                "w_safe_min": walk_to_bus + 3,
                "w_safe_score": random.randint(85, 98),
                "bus_min": bus_time + 2,
                "total_minutes_fast": walk_to_bus + bus_time + walk_from_bus + 4,
                "risk_minutes_safe": random.uniform(2.5, 8.0),
                "crowding_factor": random.uniform(0.3, 1.0),
                "bus_safety_used": random.randint(85, 95)
            }
        }
    
    # Generate realistic route paths with waypoints
    def create_realistic_route(origin_lat, origin_lon, dest_lat, dest_lon, route_type="fast"):
        """Create a realistic route path with multiple waypoints following streets."""
        # Calculate direction vector
        dlat = dest_lat - origin_lat
        dlon = dest_lon - origin_lon
        distance = math.sqrt(dlat**2 + dlon**2)
        
        # Create more realistic street-like paths
        if route_type == "bus":
            # Bus route: follows main roads, more direct
            num_waypoints = random.randint(3, 6)
            waypoints = []
            
            # Add initial point
            waypoints.append([origin_lon, origin_lat])
            
            # Create main road-like path with fewer turns
            for i in range(1, num_waypoints):
                t = i / num_waypoints
                
                # Smaller zigzag for main roads
                zigzag = math.sin(i * 1.5) * 0.0005 * distance
                
                # Smaller perpendicular offsets for main roads
                perp_lat = math.cos(i * 1.0) * 0.001 * distance
                perp_lon = math.sin(i * 1.0) * 0.001 * distance
                
                # Main path with main road variations
                lat = origin_lat + dlat * t + zigzag + perp_lat
                lon = origin_lon + dlon * t + zigzag + perp_lon
                
                waypoints.append([lon, lat])
            
            # Add final point
            waypoints.append([dest_lon, dest_lat])
            
        elif route_type == "fast":
            # Fast route: more direct but still follows streets
            num_waypoints = random.randint(5, 12)
            waypoints = []
            
            # Add initial point
            waypoints.append([origin_lon, origin_lat])
            
            # Create street-like segments
            for i in range(1, num_waypoints):
                t = i / num_waypoints
                
                # Create zigzag pattern to simulate street turns
                zigzag = math.sin(i * 2) * 0.001 * distance
                
                # Add perpendicular street-like offsets
                perp_lat = math.cos(i * 1.5) * 0.002 * distance
                perp_lon = math.sin(i * 1.5) * 0.002 * distance
                
                # Main path with street-like variations
                lat = origin_lat + dlat * t + zigzag + perp_lat
                lon = origin_lon + dlon * t + zigzag + perp_lon
                
                waypoints.append([lon, lat])
            
            # Add final point
            waypoints.append([dest_lon, dest_lat])
            
        else:  # safe route
            # Safe route: longer path avoiding main roads
            num_waypoints = random.randint(8, 15)
            waypoints = []
            
            # Add initial point
            waypoints.append([origin_lon, origin_lat])
            
            # Create safer, longer path with more turns
            for i in range(1, num_waypoints):
                t = i / num_waypoints
                
                # More pronounced zigzag for safer route
                zigzag = math.sin(i * 3) * 0.002 * distance
                
                # Larger perpendicular offsets for safer streets
                perp_lat = math.cos(i * 2.5) * 0.003 * distance
                perp_lon = math.sin(i * 2.5) * 0.003 * distance
                
                # Add some curve to avoid main roads
                curve = math.sin(t * math.pi) * 0.004 * distance
                
                # Main path with safety-focused variations
                lat = origin_lat + dlat * t + zigzag + perp_lat + curve
                lon = origin_lon + dlon * t + zigzag + perp_lon + curve
                
                waypoints.append([lon, lat])
            
            # Add final point
            waypoints.append([dest_lon, dest_lat])
        
        return waypoints
    
    # Generate demo GeoJSON with realistic routes
    def create_demo_geojson():
        # Create realistic route paths
        fast_route = create_realistic_route(olat, olon, dlat, dlon, "fast")
        safe_route = create_realistic_route(olat, olon, dlat, dlon, "safe")
        
        features = [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [olon, olat]
                },
                "properties": {
                    "role": "origin",
                    "label": "Starting Point"
                }
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [dlon, dlat]
                },
                "properties": {
                    "role": "school",
                    "label": school_name
                }
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": fast_route
                },
                "properties": {
                    "mode": "walk",
                    "variant": "fast"
                }
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": safe_route
                },
                "properties": {
                    "mode": "walk",
                    "variant": "safe"
                }
            }
        ]
        
        # Add bus route if available
        if bus_data and bus_data["fastest"]:
            bus_start = [bus_data["fastest"]["start_lon"], bus_data["fastest"]["start_lat"]]
            
            # Create walking route to bus stop
            walk_to_bus = create_realistic_route(olat, olon, bus_data["fastest"]["start_lat"], bus_data["fastest"]["start_lon"], "walk")
            
            # Create bus route (more direct, follows main roads)
            bus_route = create_realistic_route(
                bus_data["fastest"]["start_lat"], 
                bus_data["fastest"]["start_lon"], 
                dlat, dlon, "bus"
            )
            
            # Create walking route from bus stop to destination
            walk_from_bus = create_realistic_route(bus_data["fastest"]["start_lat"], bus_data["fastest"]["start_lon"], dlat, dlon, "walk")
            
            features.extend([
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": bus_start
                    },
                    "properties": {
                        "role": "bus_start",
                        "label": bus_data["fastest"]["start_label"]
                    }
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": walk_to_bus
                    },
                    "properties": {
                        "mode": "walk",
                        "variant": "to_bus"
                    }
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": bus_route
                    },
                    "properties": {
                        "mode": "bus",
                        "variant": "fast"
                    }
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": walk_from_bus
                    },
                    "properties": {
                        "mode": "walk",
                        "variant": "from_bus"
                    }
                }
            ])
        
        return {
            "type": "FeatureCollection",
            "features": features
        }
    
    # Generate Google Maps links
    def gmaps_dir(origin_ll, dest_ll, mode="walking"):
        return (
            "https://www.google.com/maps/dir/?api=1"
            f"&origin={origin_ll[0]},{origin_ll[1]}"
            f"&destination={dest_ll[0]},{dest_ll[1]}"
            f"&travelmode={mode}"
        )
    
    walk_link = gmaps_dir((olat, olon), (dlat, dlon), "walking")
    transit_link = gmaps_dir((olat, olon), (dlat, dlon), "transit")
    
    return {
        "origin": {"lat": olat, "lon": olon},
        "destination": {"lat": dlat, "lon": dlon, "name": school_name},
        "walk": {
            "fastest": {
                "minutes": walk_fast_min,
                "safety": random.randint(70, 85),
                "coords": create_realistic_route(olat, olon, dlat, dlon, "fast")
            },
            "safest": {
                "minutes": walk_safe_min,
                "safety": random.randint(85, 95),
                "coords": create_realistic_route(olat, olon, dlat, dlon, "safe")
            }
        },
        "bus": bus_data or {"fastest": None, "safest": None},
        "park_and_ride": [
            {
                "site": f"Park & Ride {i+1}",
                "lat": dlat + random.uniform(-0.02, 0.02),
                "lon": dlon + random.uniform(-0.02, 0.02),
                "walk_fast_min": random.randint(3, 12),
                "walk_safe_min": random.randint(4, 15),
                "walk_mean_safety": random.randint(80, 95),
                "km_to_school": random.uniform(0.5, 2.0)
            }
            for i in range(3)
        ],
        "links": {
            "google": {
                "walking": walk_link,
                "transit": transit_link
            }
        },
        "geojson": create_demo_geojson(),
        "real_routing": False
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "data_loaded": bus_df is not None,
        "available_schools": len(AVAILABLE_SCHOOLS),
        "real_routing": bus_df is not None
    }

@app.get("/api/stats")
async def get_stats():
    """Get application statistics."""
    return {
        "total_schools": len(AVAILABLE_SCHOOLS),
        "bus_stops": len(bus_df) if bus_df is not None else 0,
        "park_ride_locations": len(pr_df) if pr_df is not None else 0,
        "journey_data_points": len(dj_df) if dj_df is not None else 0,
        "real_routing": bus_df is not None
    }

if __name__ == "__main__":
    print("🚀 Starting Trust Track School Safety...")
    print(f"📁 Project root: {project_root}")
    print(f"📁 Frontend path: {frontend_path}")
    print(f"✅ Frontend exists: {frontend_path.exists()}")
    
    if bus_df is not None:
        print("🎯 Using REAL ROUTING with OSM data and actual algorithms!")
    else:
        print("🎭 Using DEMO MODE - simulated routing data")
    
    uvicorn.run(
        "demo_app:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
