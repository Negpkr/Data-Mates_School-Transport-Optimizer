# Risk Calculation Module

A comprehensive road safety analysis module that calculates crash density and risk assessment for major roads in the Canberra area using historical crash data and geographic analysis.

## Overview

The Risk Calculation module provides sophisticated analysis of road safety by calculating crash density along major road segments. This analysis helps identify high-risk areas and supports route planning decisions for safer school journeys.

## Features

### Crash Density Analysis
- **Geographic Crash Mapping**: Maps historical crash points to specific road segments
- **Distance-based Analysis**: Calculates crash density within 1km of major roads
- **Multi-road Assessment**: Analyzes multiple major road segments simultaneously
- **Statistical Calculations**: Provides crash density metrics per kilometer

### Road Segments Analyzed
- **Northbourne Avenue**: Major arterial road through Canberra
- **Gungahlin Drive**: Key connecting road in northern Canberra
- **Barton Highway**: Important highway connecting Canberra to NSW
- **Parkes Way**: Major thoroughfare in central Canberra

## Files

### calculations.py
The main Python script that performs the crash density calculations.

**Key Components:**
- Geographic coordinate definitions for road segments
- Historical crash point database (2015-2021)
- Distance calculation algorithms
- Crash density computation

### riskCalculation.docx
Detailed documentation and analysis report in Word format.

## Technical Implementation

### Dependencies
```python
from geopy.distance import geodesic
from shapely.geometry import LineString, Point
from pyproj import Geod
import numpy
```

### Core Functions

#### Road Segment Definition
```python
# Define road segments as LineString objects
line_NorthBAven = LineString([(-35.275707,149.129453), (-35.240601,149.137072)])
line_GungDr = LineString([(-35.224321,149.121756), (-35.257097,149.089787)])
line_BartonHwy = LineString([(-35.240601,149.137072),(-35.224321,149.121756)])
line_ParkesWay = LineString([(-35.257097,149.089787),(-35.275707,149.129453)])
```

#### Crash Point Database
The module includes a comprehensive database of crash points from 2015-2021:
- **2015**: 12 crash points
- **2016**: 8 crash points  
- **2017**: 8 crash points
- **2018**: 8 crash points
- **2019**: 8 crash points
- **2020**: 5 crash points
- **2021**: 3 crash points

**Total**: 52 historical crash points

#### Distance Calculation
```python
# Calculate distance between crash points and road segments
result = geod.inv(pt.x, pt.y, pointsOnLine.y, pointsOnLine.x)
distance_km = result[2]/1000
```

#### Crash Density Formula
```python
crash_density = number_of_crashes_within_1km / road_segment_length_km
```

## Usage

### Running the Analysis
```bash
cd riskCalculation
python calculations.py
```

### Output
The script provides:
1. **Individual crash point analysis**: Distance from each crash point to road segments
2. **Road segment statistics**: Length and crash count for each road
3. **Crash density results**: Final density calculations for each road segment

### Example Output
```
Distance between point234892_15 and NorthBAvenue is: 0.8 km
The length of the line NorthBAvenue Road is: 4.2
Distance between point231209_15 and GungDr is: 0.3 km
The length of the line GungDr Road is: 3.8
...
The crash density in road NorthBAvenue, GungDr, BartonHwy, and ParkesWay are: 
[crash_density_values]
```

## Methodology

### Geographic Analysis
1. **Road Segmentation**: Major roads are defined as LineString objects using GPS coordinates
2. **Crash Point Mapping**: Historical crash points are mapped to Point objects
3. **Distance Calculation**: Geodesic distance is calculated between crash points and road segments
4. **Proximity Filtering**: Only crashes within 1km of road segments are counted
5. **Density Calculation**: Crash count is divided by road segment length

### Data Sources
- **Crash Data**: Historical crash records from ACT government sources
- **Road Coordinates**: GPS coordinates for major road segments
- **Time Period**: 2015-2021 crash data for trend analysis

## Safety Implications

### High-Risk Areas
- Roads with higher crash density indicate increased risk
- Areas with multiple crashes in close proximity
- Intersections and merging points often show higher density

### Route Planning Applications
- **Avoid High-Density Areas**: Route planning can prioritize lower-risk roads
- **Safety Scoring**: Crash density contributes to overall route safety scores
- **Temporal Analysis**: Different time periods show varying risk patterns

## Integration with Trust Track

### Route Safety Scoring
The crash density data is integrated into the Trust Track application to:
- **Calculate route safety scores**
- **Prioritize safer road segments**
- **Provide safety recommendations**
- **Support parent decision-making**

### Real-time Updates
- Crash density data is updated periodically
- New crash data is incorporated into calculations
- Safety scores are adjusted based on recent incidents

## Data Quality

### Accuracy
- **GPS Precision**: Crash points use high-precision GPS coordinates
- **Road Alignment**: Road segments are accurately mapped
- **Distance Calculations**: Geodesic calculations account for Earth's curvature

### Limitations
- **Historical Data**: Analysis based on past crash data
- **Proximity Threshold**: 1km radius may not capture all relevant crashes
- **Road Changes**: New road infrastructure may not be reflected in historical data

## Future Enhancements

### Planned Improvements
- **Real-time Data Integration**: Live crash data feeds
- **Weather Correlation**: Crash patterns during different weather conditions
- **Time-based Analysis**: Crash patterns by time of day and season
- **Pedestrian-Specific Analysis**: Focus on pedestrian-involved crashes
- **School Zone Analysis**: Special focus on areas near schools

### Advanced Analytics
- **Machine Learning**: Predictive crash risk modeling
- **Traffic Flow Integration**: Correlation with traffic volume data
- **Infrastructure Analysis**: Impact of road improvements on safety

## Contributing

### Adding New Crash Data
1. Update the `crashPoints` dictionary with new coordinates
2. Follow the naming convention: `point[ID]_[YEAR]`
3. Ensure GPS coordinates are in (latitude, longitude) format
4. Re-run calculations to update density metrics

### Adding New Road Segments
1. Define new road coordinates as LineString
2. Add distance calculation logic
3. Update crash density calculations
4. Test with existing crash point data

## Support

For questions about the risk calculation module:
- **Technical Issues**: Check the calculations.py file for implementation details
- **Data Questions**: Refer to riskCalculation.docx for detailed analysis
- **Integration Help**: See the main project README.md for Trust Track integration

---

**Risk Calculation Module** - Supporting safer school journeys through data-driven safety analysis.
