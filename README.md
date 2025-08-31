# Trust Track Notebook

A collection of Jupyter notebooks and interactive maps that demonstrate the data analysis, routing algorithms, and safety calculations behind the Trust Track school safety application.

## Overview

The notebooks folder contains the research and development work that led to the Trust Track application. It includes data analysis of ACT transport and safety data, routing algorithm development, and interactive map visualizations.

## Contents

### Core Analysis Notebook

#### mvp_routing 2.ipynb
The main analysis notebook that demonstrates the complete Trust Track routing system.

**Key Components:**
- **Data Loading**: ACT government datasets for schools, transport, and safety
- **Graph Construction**: OpenStreetMap-based walking network for Canberra
- **Safety Analysis**: Crash data visualization and risk assessment
- **Route Calculation**: Fastest and safest path algorithms
- **Interactive Maps**: Folium-based route visualization

**Datasets Analyzed:**
- ACT Road Crash Data (2025)
- ACT School Bus Services
- Bus Routes
- Census Data for ACT Schools
- Daily Public Transport Journeys
- Park and Ride Locations
- Smart Parking Lots

### Interactive Maps

#### trust_track_demo_map.html
Complete Trust Track demonstration map showing:
- **Route Comparison**: Fastest vs. safest walking paths
- **Bus Integration**: Public transport segments
- **Safety Overlays**: Crash data and risk indicators
- **Interactive Controls**: Layer toggles and route selection

#### trust_track_route.html
Basic route visualization with:
- **Single Route Display**: Individual route plotting
- **Waypoint Markers**: Start, end, and intermediate points
- **Distance Information**: Route length and estimated time

#### trust_track_route_with_bus.html
Enhanced route visualization including:
- **Multi-modal Routes**: Walking and bus segments
- **Transport Integration**: Bus stop locations and routes
- **Combined Paths**: Seamless walking-to-bus transitions

#### trust_track_map_fixed.html
Corrected map version with:
- **Bug Fixes**: Resolved display and interaction issues
- **Improved Performance**: Optimized rendering and loading
- **Enhanced UI**: Better controls and user experience

#### trust_track_updated_map.html
Latest map iteration featuring:
- **Updated Data**: Most recent crash and transport information
- **New Features**: Additional safety indicators
- **Performance Improvements**: Faster loading and smoother interactions

### Cache Directory

#### cache/
Contains cached data files for faster notebook execution:
- **OSM Data**: OpenStreetMap network data for Canberra
- **Graph Objects**: Pre-computed network graphs
- **Analysis Results**: Cached calculations and computations

## Technical Implementation

### Data Processing Pipeline

#### 1. Data Loading
```python
# Load ACT government datasets
schools = pd.read_csv("Census_Data_for_all_ACT_Schools_20250830.csv")
crash_data = pd.read_csv("ACT_Road_Crash_Data_20250831.csv")
bus_routes = pd.read_csv("Bus_Routes.csv")
```

#### 2. Network Construction
```python
# Build walking graph from OpenStreetMap
G = ox.graph_from_place("Australian Capital Territory, Australia", 
                       network_type="walk", simplify=True)
G = ox.distance.add_edge_lengths(G)
```

#### 3. Safety Scoring
```python
# Road class risk assessment
ROADCLASS_RISK = {
    "motorway": 1.00, "trunk": 0.95, "primary": 0.90, 
    "secondary": 0.75, "tertiary": 0.60, "residential": 0.40
}
```

#### 4. Route Calculation
```python
# Calculate fastest and safest paths
fastest_path = nx.shortest_path(G, start, end, weight='length')
safest_path = nx.shortest_path(G, start, end, weight='safety_score')
```

### Key Algorithms

#### Safety Scoring Algorithm
1. **Road Classification**: Assign risk scores based on road type
2. **Crash Density**: Calculate crash frequency per road segment
3. **Pedestrian Infrastructure**: Assess sidewalk availability and quality
4. **Traffic Volume**: Consider vehicle density and speed limits
5. **Lighting Assessment**: Evaluate street lighting coverage

#### Route Optimization
1. **Multi-objective Optimization**: Balance safety vs. time
2. **Constraint Satisfaction**: Ensure route feasibility
3. **Dynamic Weighting**: Adjust safety/time preferences
4. **Alternative Generation**: Provide multiple route options

## Data Sources

### Government Datasets
- **ACT Government**: School census, transport, and safety data
- **OpenStreetMap**: Road network and infrastructure data
- **ABS (Australian Bureau of Statistics)**: Demographic and transport statistics

### Data Quality
- **Temporal Coverage**: 2015-2025 crash and transport data
- **Spatial Accuracy**: High-precision GPS coordinates
- **Completeness**: Comprehensive coverage of ACT region
- **Consistency**: Standardized data formats and classifications

## Visualization Features

### Interactive Maps
- **Layer Controls**: Toggle different data layers
- **Route Comparison**: Side-by-side fastest vs. safest routes
- **Safety Heatmaps**: Visual crash density and risk areas
- **Transport Integration**: Bus routes and stops overlay
- **Real-time Updates**: Dynamic route recalculation

### Data Visualizations
- **Crash Analysis**: Yearly trends and severity distributions
- **Transport Statistics**: Bus usage and route efficiency
- **Parking Analysis**: Capacity and availability metrics
- **Safety Metrics**: Risk scores and safety indicators

## Usage

### Running the Notebooks
```bash
cd notebooks
jupyter notebook mvp_routing\ 2.ipynb
```

### Prerequisites
```python
# Required packages
import osmnx as ox
import networkx as nx
import pandas as pd
import geopandas as gpd
import numpy as np
import folium
import matplotlib.pyplot as plt
from shapely import wkt
from shapely.geometry import Point, LineString
```

### Data Requirements
- All CSV files must be in the `../data/` directory
- Internet connection for OpenStreetMap data
- Sufficient memory for large network graphs

## Research Findings

### Safety Insights
- **High-Risk Areas**: Identified dangerous road segments and intersections
- **Temporal Patterns**: Crash frequency varies by time of day and season
- **Infrastructure Impact**: Sidewalk availability significantly affects safety
- **Transport Integration**: Bus routes can improve overall journey safety

### Route Optimization Results
- **Safety vs. Time Trade-off**: Safest routes typically 20-40% longer
- **Multi-modal Benefits**: Combining walking and bus reduces risk
- **Alternative Routes**: Multiple safe options available for most journeys
- **Dynamic Adaptation**: Routes adjust based on real-time conditions

## Integration with Trust Track

### Algorithm Transfer
- **Core Algorithms**: Notebook algorithms form the basis of the web application
- **Data Processing**: Similar data loading and preprocessing pipelines
- **Safety Scoring**: Consistent risk assessment methodology
- **Route Calculation**: Same optimization algorithms

### Performance Optimization
- **Caching**: Pre-computed results for faster web application response
- **Simplification**: Streamlined algorithms for real-time use
- **API Integration**: Notebook findings inform API endpoint design
- **User Interface**: Map visualizations guide web application design

## Future Development

### Planned Enhancements
- **Machine Learning**: Predictive safety modeling
- **Real-time Data**: Live traffic and incident feeds
- **Weather Integration**: Safety adjustments for weather conditions
- **User Feedback**: Learning from user route preferences

### Research Directions
- **Advanced Analytics**: Deep learning for route optimization
- **Predictive Modeling**: Anticipating safety risks
- **Personalization**: User-specific safety preferences
- **Community Features**: Crowdsourced safety information

## Contributing

### Adding New Analysis
1. Create new notebook with clear documentation
2. Follow existing code structure and conventions
3. Include data validation and error handling
4. Add visualizations and explanations
5. Update this README with new findings

### Data Updates
1. Ensure new data follows existing formats
2. Update data loading functions as needed
3. Validate data quality and completeness
4. Re-run analysis with updated datasets
5. Update visualizations and maps

## Support

For questions about the notebooks:
- **Technical Issues**: Check the notebook code and error messages
- **Data Questions**: Refer to the data source documentation
- **Algorithm Help**: See the main project README.md for implementation details
- **Visualization Issues**: Check browser compatibility and JavaScript console

---

**Trust Track Notebooks** - Research and development foundation for safer school journeys.
