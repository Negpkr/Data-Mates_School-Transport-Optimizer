# Trust Track Web Application

A modern, safety-focused web application for planning secure routes to school using public transport, school buses, and walking paths.

![Trust Track Web App](https://img.shields.io/badge/Trust%20Track-Web%20Application-blue?style=for-the-badge&logo=shield)

## 🌐 Live Application

**Access the application:** http://localhost:8000

## 🎯 Overview

Trust Track is a comprehensive web-based school safety routing application designed to help parents and students find the safest routes to school. The application combines real-time public transport data, school bus services, and safety analytics to provide peace of mind for school journeys.

## ✨ Key Features

### 🛡️ Safety-First Design
- **Safety Scoring**: Every route is evaluated for safety factors
- **Well-lit Paths**: Prioritizes routes with good lighting
- **Population Density**: Favors populated, well-monitored areas
- **Traffic Patterns**: Considers pedestrian-friendly routes

### 🚌 Multi-Modal Transport
- **Public Transport**: Integration with Canberra's public transport network
- **School Buses**: Dedicated school bus services and routes
- **Walking Routes**: Safe pedestrian paths with safety overlays
- **Park & Ride**: Convenient parking and transport options

### 📱 Modern User Interface
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Interactive Maps**: Real-time route visualization with Leaflet.js
- **Intuitive Navigation**: Clean, modern interface with clear icons
- **Real-time Updates**: Live bus tracking and arrival predictions

## 🖥️ Application Screenshots

### Main Interface

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

## 🚀 How to Use

### Getting Started

1. **Open the Application**
   - Navigate to http://localhost:8000
   - The application will load with the main interface

2. **Plan Your First Route**
   - Enter your starting point (address or use GPS)
   - Select your child's school from the dropdown
   - Choose your preferred departure date and time
   - Click "Plan Route" to see available options

3. **Compare Route Options**
   - **Recommended Route**: Best overall option (safety + time)
   - **Walking Route**: Safe pedestrian path
   - **Fastest Route**: Quickest option (may use busier roads)
   - Each route shows safety score and estimated time

### Using the Interactive Map

- **Toggle Route Types**: Use the map controls to show/hide different routes
- **Zoom and Pan**: Navigate the map to explore your route
- **Safety Overlays**: View safety information and bus stops
- **Real-time Updates**: See live bus locations and arrival times

### Safety Features

- **Safety Scoring**: Every route displays a safety percentage
- **Incident Reporting**: Report safety concerns at any location
- **Live Tracking**: Monitor bus locations in real-time
- **Safety Alerts**: Receive notifications about route changes

### User Settings

- **Profile Management**: Manage your child's safety preferences
- **Notification Settings**: Customize safety alerts and updates
- **Route Preferences**: Set safety vs. speed priorities
- **Transport Preferences**: Choose preferred transport modes

## 🛠️ Technical Features

### Frontend Technologies
- **HTML5/CSS3**: Modern, responsive design
- **JavaScript**: Interactive features and real-time updates
- **Leaflet.js**: Interactive mapping and route visualization
- **Font Awesome**: Professional iconography

### User Experience
- **Mobile-First Design**: Optimized for all device sizes
- **Accessibility**: High contrast, readable fonts, keyboard navigation
- **Performance**: Fast loading times and smooth interactions
- **Intuitive Interface**: Clear navigation and helpful tooltips

### Real-Time Features
- **Live Bus Tracking**: Real-time location updates
- **Dynamic Route Updates**: Automatic re-routing for safety
- **Safety Alerts**: Immediate notifications for incidents
- **Interactive Maps**: Real-time route visualization

## 📱 Browser Compatibility

- **Chrome**: Full support (recommended)
- **Firefox**: Full support
- **Safari**: Full support
- **Edge**: Full support
- **Mobile Browsers**: Optimized for iOS Safari and Chrome Mobile

## 🔧 Troubleshooting

### Common Issues

1. **Map Not Loading**
   - Check your internet connection
   - Refresh the page
   - Clear browser cache

2. **Route Planning Fails**
   - Verify your starting point is valid
   - Check that the school is selected
   - Ensure date and time are set correctly

3. **Slow Performance**
   - Close other browser tabs
   - Check your internet connection
   - Try refreshing the page

### Getting Help

- **API Documentation**: http://localhost:8000/docs
- **Interactive Testing**: http://localhost:8000/redoc
- **Browser Console**: Check for JavaScript errors (F12)

## 🎨 Design Principles

### User-Centered Design
- **Safety First**: Every feature prioritizes user safety
- **Simplicity**: Clean, intuitive interface
- **Accessibility**: Inclusive design for all users
- **Responsiveness**: Works on all devices and screen sizes

### Visual Design
- **Modern Aesthetics**: Clean lines and professional appearance
- **Color Psychology**: Blue for trust, green for safety
- **Typography**: Readable fonts with proper hierarchy
- **Icons**: Clear, meaningful iconography

## 📊 Performance Metrics

- **Page Load Time**: < 3 seconds
- **Route Calculation**: < 5 seconds
- **Map Rendering**: < 2 seconds
- **API Response**: < 1 second
- **Mobile Performance**: Optimized for mobile networks

## 🔒 Privacy & Security

- **Data Protection**: No personal data stored
- **Secure Connections**: HTTPS encryption
- **Privacy Compliance**: Meets Australian privacy standards
- **Local Processing**: Route calculations done locally

## 🌟 Future Enhancements

- **Weather Integration**: Route planning based on weather conditions
- **Parent Notifications**: SMS/email alerts for route changes
- **Route History**: Track and analyze past journeys
- **Community Features**: Share safe routes with other parents
- **Multi-language Support**: Support for additional languages

## 📁 Webpage Structure

```
webpage/
├── README.md              # This file - Web application documentation
└── screenshots/           # Application screenshots
    ├── WebApp.png         # Main application interface
    ├── Map.png            # Interactive map view
    ├── Profile.png        # User profile management
    ├── setting.png        # Application settings
    ├── onboarding_*.png   # Onboarding flow screenshots
    ├── trip_planner_*.png # Trip planning features
    ├── school_buses_*.png # School bus management
    ├── live_bus_*.png     # Live tracking features
    ├── report_*.png       # Safety reporting features
    └── localhost-doc-*.png # API documentation
```

---

**Trust Track Web Application** - Making school journeys safer, one route at a time. 🚌🛡️

*For technical documentation and API reference, see the main project README.md file.*
