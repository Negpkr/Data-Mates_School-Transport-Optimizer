# Trust Track - School Safety Demo

A comprehensive school safety routing application designed to help parents and students find the safest routes to school using public transport, school buses, and walking paths.

![Trust Track Logo](https://img.shields.io/badge/Trust%20Track-School%20Safety-blue?style=for-the-badge&logo=shield)

## 🎯 Overview

Trust Track is a modern web application that prioritizes student safety when planning routes to school. It combines real-time public transport data, school bus services, and safety analytics to provide parents with peace of mind and students with secure travel options.

## ✨ Key Features

- **Safety-First Routing**: Prioritizes well-lit, populated routes with high safety scores
- **Multi-Modal Transport**: Public transport, school buses, and walking options
- **Real-Time Tracking**: Live bus tracking and arrival predictions
- **Interactive Maps**: Visual route planning with safety overlays
- **School Integration**: Direct integration with ACT school bus services
- **Parent Dashboard**: Comprehensive safety monitoring and alerts
- **Mobile Responsive**: Works seamlessly on all devices

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd school-safety-demo
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
 
## 📱 Application Screenshots

### Main Application Interface

#### Web Application Overview
![Web Application](screenshots/WebApp.png)
*Main Trust Track interface with trip planner and interactive map*

#### Interactive Map
![Interactive Map](screenshots/Map.png)
*Real-time map with route visualization and safety overlays*

### Trip Planning Features

#### Start Point Selection
![Start Point](screenshots/start_point.png)
*Choose your starting location with GPS integration*

#### Destination Planning
![Destination](screenshots/Destination.png)
*Select school destinations with safety scoring*

#### Walking Route Planning
![Walking Route](screenshots/destination-walk.png)
*Safe walking routes with pedestrian-friendly paths*

### User Interface Components

#### Profile Management
![Profile](screenshots/Profile.png)
*User profile and child safety settings management*

#### Application Settings
![Settings](screenshots/setting.png)
*Customize safety preferences and notification settings*

### Onboarding Experience

#### Welcome Screen
![Welcome Screen](screenshots/onboarding_01_welcome.png)
*Get started with Trust Track's comprehensive safety features*

#### School Selection
![School Selection](screenshots/onboarding_02_select_school.png)
*Choose your child's school from the ACT school network*

#### Myki Card Integration
![Myki Integration](screenshots/onboarding_03_link_myki.png)
*Link your Myki card for seamless public transport access*

#### Safety Preferences
![Safety Preferences](screenshots/onboarding_04_set_preferences.png)
*Customize safety settings and route preferences*

#### Notifications Setup
![Notifications](screenshots/onboarding_05_enable_notifications.png)
*Enable real-time safety alerts and route updates*

#### Setup Complete
![Setup Complete](screenshots/onboarding_06_done.png)
*You're all set! Start planning safe routes*

### Core Features

#### Trip Planner - Public Transport
![Public Transport Planner](screenshots/trip_planner_public.png)
*Plan routes using Canberra's public transport network*

#### Trip Planner - School Bus
![School Bus Planner](screenshots/trip_planner_school_bus.png)
*Access dedicated school bus services*

#### School Bus List
![School Bus List](screenshots/school_buses_list.png)
*Browse available school bus routes and schedules*

#### School Bus Filtering
![School Bus Filter](screenshots/school_buses_filter.png)
*Filter buses by school, time, and safety rating*

#### Route Details
![Route Details](screenshots/route_details_school_bus.png)
*Detailed view of selected route with safety information*

### Safety Features

#### Live Bus Tracking
![Live Tracking](screenshots/live_bus_tracking.png)
*Real-time bus location and arrival predictions*

#### Report Unsafe Stop
![Report Form](screenshots/report_unsafe_stop_form.png)
*Report safety concerns at bus stops or along routes*

#### Report Submitted
![Report Submitted](screenshots/report_unsafe_stop_submitted.png)
*Confirmation of safety report submission*

### User Management

#### Profile Management
![Profile](screenshots/profile_my_child.png)
*Manage your child's safety settings and preferences*

#### Application Settings
![Settings](screenshots/settings.png)
*Customize app preferences and safety thresholds*

### API Documentation

#### Interactive API Docs
![API Documentation](screenshots/localhost-doc-1.png)
*Comprehensive API documentation with interactive testing*

#### API Endpoints
![API Endpoints](screenshots/localhost-doc-2.png)
*Detailed endpoint documentation and examples*

#### API Testing Interface
![API Testing](screenshots/localhost-doc-3.png)
*Test API endpoints directly from the documentation*

## 📁 Project Structure

```
school-safety-demo/
├── app.py                 # Main FastAPI application
├── run.py                # Application startup script
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── frontend/             # Frontend files
│   ├── index.html        # Main HTML page
│   ├── styles.css        # CSS styles
│   └── app.js           # JavaScript functionality
├── trusttrack/           # Backend routing logic
│   ├── api.py           # Original API endpoints
│   ├── routing.py       # Route computation
│   └── utils.py         # Utility functions
├── data/                 # Data files (CSV)
│   ├── ACT_School_Bus_Services.csv
│   ├── Bus_Routes.csv
│   ├── Census_Data_for_all_ACT_Schools_20250830.csv
│   ├── Daily_Public_Transport_Passenger_Journeys_by_Service_Type_20250830.csv
│   └── Park_And_Ride_Locations.csv
├── screenshots/          # Application screenshots
│   ├── WebApp.png        # Main application interface
│   ├── Map.png           # Interactive map view
│   ├── Profile.png       # User profile management
│   ├── setting.png       # Application settings
│   ├── onboarding_*.png  # Onboarding flow screenshots
│   ├── trip_planner_*.png # Trip planning features
│   ├── school_buses_*.png # School bus management
│   ├── live_bus_*.png    # Live tracking features
│   ├── report_*.png      # Safety reporting features
│   └── localhost-doc-*.png # API documentation
├── mockups/              # Original design mockups
└── notebooks/            # Jupyter notebooks (original analysis)
```

## 🏗️ Architecture

### Frontend
- **HTML5/CSS3**: Modern, responsive design
- **JavaScript**: Interactive features and real-time updates
- **Leaflet.js**: Interactive mapping and route visualization
- **Font Awesome**: Professional iconography

### Backend
- **FastAPI**: High-performance Python web framework
- **OSMnx**: OpenStreetMap data processing
- **NetworkX**: Graph-based routing algorithms
- **Pandas**: Data manipulation and analysis

### Data Sources
- **ACT School Bus Services**: Official school transport data
- **Park & Ride Locations**: Public transport hubs
- **Public Transport Journeys**: Real-time passenger data
- **Census Data**: Demographic and safety analytics

## 🔧 API Endpoints

### Core Routing
- `GET /api/route` - Calculate optimal routes
- `GET /api/schools` - List available schools
- `GET /api/buses` - School bus services
- `GET /api/safety` - Safety analytics

### User Management
- `POST /api/report` - Submit safety reports
- `GET /api/profile` - User preferences
- `PUT /api/settings` - Update settings

## 📊 Safety Features

### Route Safety Scoring
- **Well-lit paths**: Prioritizes routes with good lighting
- **Population density**: Favors populated areas
- **Crime statistics**: Integrates local safety data
- **Traffic patterns**: Considers pedestrian-friendly routes

### Real-Time Monitoring
- **Live tracking**: Real-time bus and route monitoring
- **Safety alerts**: Immediate notifications for incidents
- **Route alternatives**: Automatic re-routing for safety

## 🛡️ Privacy & Security

- **Data encryption**: All sensitive data is encrypted
- **Privacy compliance**: Meets Australian privacy standards
- **Secure APIs**: Protected endpoints with authentication
- **Local processing**: Route calculations done locally

## 🤝 Contributing

We welcome contributions to improve Trust Track! Please see our contributing guidelines for details on:

- Code style and standards
- Testing requirements
- Pull request process
- Issue reporting

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **ACT Government**: For providing transport and safety data
- **OpenStreetMap**: For mapping and routing data
- **Canberra Public Transport**: For real-time service information

## 📞 Support

For support and questions:
- **Email**: support@trusttrack.com.au
- **Documentation**: http://localhost:8000/docs
- **Issues**: GitHub Issues page

---

**Trust Track** - Making school journeys safer, one route at a time. 🚌🛡️
