# Trust Track Application

The main web application for Trust Track - a school safety routing system that helps parents and students find the safest routes to school.

## Overview

This folder contains the complete web application including the FastAPI backend, frontend interface, and all necessary configuration files to run the Trust Track system.

## Contents

### Core Application Files

#### app.py
The main FastAPI application that provides:
- **API Endpoints**: Route calculation, school data, and safety analytics
- **Data Integration**: ACT government datasets and OpenStreetMap data
- **Safety Algorithms**: Risk assessment and route optimization
- **Real-time Features**: Live bus tracking and safety alerts

#### demo_app.py
A demonstration application showcasing:
- **Core Features**: Basic routing and safety analysis
- **API Examples**: Sample requests and responses
- **Testing Interface**: Interactive testing of application features

#### run.py
Application startup script that:
- **Environment Setup**: Checks Python version and dependencies
- **Data Validation**: Ensures all required data files are present
- **Server Launch**: Starts the FastAPI server with proper configuration
- **Error Handling**: Comprehensive error checking and user feedback

#### requirements.txt
Python dependencies required for the application:
- **FastAPI**: High-performance web framework
- **OSMnx**: OpenStreetMap data processing
- **NetworkX**: Graph-based routing algorithms
- **Pandas**: Data manipulation and analysis
- **Shapely**: Geometric calculations

### Frontend Application

#### frontend/
Complete web interface including:

**index.html**
- Main HTML page with responsive design
- Interactive map integration with Leaflet.js
- Modern UI components and navigation

**styles.css**
- Professional styling and layout
- Mobile-responsive design
- Accessibility features and animations

**app.js**
- Interactive features and real-time updates
- Map controls and route visualization
- API integration and data handling

### Backend Logic

#### trusttrack/
Core routing and safety analysis module:

**api.py**
- RESTful API endpoints
- Request/response handling
- Data validation and error management

**routing.py**
- Route calculation algorithms
- Safety scoring and optimization
- Multi-modal transport integration

**utils.py**
- Utility functions and helpers
- Data processing and formatting
- Geographic calculations

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Modern web browser

### Installation

1. **Navigate to application folder**
   ```bash
   cd application
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python3 run.py
   ```

4. **Access the application**
   - Open your browser to: http://localhost:8000
   - API documentation: http://localhost:8000/docs

## Application Features

### Route Planning
- **Multi-modal Transport**: Walking, public transport, and school buses
- **Safety Scoring**: Data-driven safety assessment for each route
- **Real-time Updates**: Live bus tracking and route adjustments
- **Alternative Routes**: Multiple options with different safety/time trade-offs

### Safety Analysis
- **Crash Data Integration**: Historical crash records and risk assessment
- **Infrastructure Analysis**: Sidewalk availability and lighting assessment
- **Population Density**: Well-monitored vs. isolated area analysis
- **Traffic Patterns**: Pedestrian-friendly route identification

### User Interface
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Interactive Maps**: Real-time route visualization
- **Intuitive Navigation**: Clean, modern interface
- **Accessibility**: High contrast and keyboard navigation support

## API Endpoints

### Core Routing
- `GET /api/route` - Calculate optimal routes between points
- `GET /api/schools` - List available schools and locations
- `GET /api/buses` - School bus services and schedules
- `GET /api/safety` - Safety analytics and risk assessment

### User Management
- `POST /api/report` - Submit safety reports and incidents
- `GET /api/profile` - User preferences and settings
- `PUT /api/settings` - Update safety and route preferences

## Data Sources

### ACT Government Data
- **School Census**: Location and enrollment data for all ACT schools
- **Transport Data**: Bus routes, schedules, and school bus services
- **Safety Data**: Historical crash records and incident reports
- **Infrastructure**: Park and ride locations and smart parking

### OpenStreetMap Data
- **Road Networks**: Complete street network for Canberra
- **Pedestrian Infrastructure**: Sidewalks, crossings, and paths
- **Public Transport**: Bus stops and route information
- **Geographic Features**: Parks, landmarks, and boundaries

## Performance

### Current Metrics
- **Page Load Time**: < 3 seconds
- **Route Calculation**: < 5 seconds for complex routes
- **Map Rendering**: < 2 seconds with cached data
- **API Response**: < 1 second for most requests

### Optimization Features
- **Caching**: Pre-computed results for faster response
- **Efficient Algorithms**: Optimized routing and safety calculations
- **Data Compression**: Minimized data transfer and storage
- **Lazy Loading**: On-demand data loading for better performance

## Development

### Code Structure
- **Modular Design**: Separate concerns for frontend, backend, and data
- **Clean Architecture**: Well-organized file structure
- **Documentation**: Comprehensive code comments and docstrings
- **Error Handling**: Robust error management and user feedback

### Testing
- **API Testing**: Comprehensive endpoint testing
- **Frontend Testing**: User interface validation
- **Integration Testing**: End-to-end functionality verification
- **Performance Testing**: Load and stress testing

## Troubleshooting

### Common Issues

1. **Dependencies Not Found**
   ```bash
   pip install -r requirements.txt
   ```

2. **Data Files Missing**
   - Ensure all CSV files are in the `../data/` directory
   - Check file permissions and accessibility

3. **Port Already in Use**
   - Change port in run.py or kill existing process
   - Use `lsof -i :8000` to find process using port 8000

4. **Map Not Loading**
   - Check internet connection for OpenStreetMap data
   - Clear browser cache and refresh page

### Getting Help
- **API Documentation**: http://localhost:8000/docs
- **Interactive Testing**: http://localhost:8000/redoc
- **Error Logs**: Check console output for detailed error messages
- **Browser Console**: F12 for frontend debugging

## Security

### Data Protection
- **No Personal Data**: All calculations done locally
- **Secure Connections**: HTTPS encryption for all data
- **Privacy Compliance**: Meets Australian privacy standards
- **Anonymous Usage**: No tracking of individual users

### API Security
- **Input Validation**: All user inputs are validated
- **Error Handling**: Secure error messages without exposing internals
- **Rate Limiting**: Protection against abuse and overload
- **CORS Configuration**: Proper cross-origin resource sharing

## Future Enhancements

### Planned Features
- **Machine Learning**: Predictive safety modeling
- **Weather Integration**: Route adjustments for weather conditions
- **Parent Notifications**: SMS/email alerts for route changes
- **Community Features**: Crowdsourced safety information

### Technical Improvements
- **Real-time Data**: Live traffic and incident feeds
- **Advanced Analytics**: Deep learning for route optimization
- **Mobile App**: Native iOS and Android applications
- **Cloud Deployment**: Scalable cloud infrastructure

---

**Trust Track Application** - The core web application for safer school journeys.

*For project overview and documentation, see the main README.md file.*
