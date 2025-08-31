// Trust Track App - Frontend JavaScript

class TrustTrackApp {
    constructor() {
        this.map = null;
        this.currentRoute = null;
        this.routeLayers = {
            fast: null,
            safe: null,
            bus: null
        };
        this.markers = [];
        
        this.init();
    }

    init() {
        this.initializeMap();
        this.bindEvents();
        this.setDefaultDate();
        this.loadFromURL();
    }

    initializeMap() {
        // Initialize map
        this.map = L.map('map').setView([-35.281, 149.128], 13);
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap contributors'
        }).addTo(this.map);

        // Add custom map controls
        this.addMapControls();
    }

    addMapControls() {
        // Map control buttons functionality
        const controls = ['toggleFast', 'toggleSafe', 'toggleBus'];
        controls.forEach(controlId => {
            const btn = document.getElementById(controlId);
            if (btn) {
                btn.addEventListener('click', (e) => {
                    e.preventDefault();
                    this.toggleMapLayer(controlId);
                });
            }
        });
    }

    toggleMapLayer(controlId) {
        const btn = document.getElementById(controlId);
        const layerType = controlId.replace('toggle', '').toLowerCase();
        
        // Toggle button state
        btn.classList.toggle('active');
        
        // Toggle layer visibility
        if (this.routeLayers[layerType]) {
            if (this.map.hasLayer(this.routeLayers[layerType])) {
                this.map.removeLayer(this.routeLayers[layerType]);
            } else {
                this.map.addLayer(this.routeLayers[layerType]);
            }
        }
    }

    bindEvents() {
        // Transport mode toggle
        document.querySelectorAll('.toggle-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.toggle-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
            });
        });

        // Use location button
        document.getElementById('useLocationBtn').addEventListener('click', () => {
            this.getCurrentLocation();
        });

        // Plan route button
        document.getElementById('planRouteBtn').addEventListener('click', () => {
            this.planRoute();
        });

        // Back to planner button
        document.getElementById('backToPlanner').addEventListener('click', () => {
            this.showPlanner();
        });

        // Modal controls
        document.getElementById('settingsBtn').addEventListener('click', () => {
            this.showModal('settingsModal');
        });

        document.getElementById('profileBtn').addEventListener('click', () => {
            this.showModal('profileModal');
        });

        document.getElementById('closeSettings').addEventListener('click', () => {
            this.hideModal('settingsModal');
        });

        document.getElementById('closeProfile').addEventListener('click', () => {
            this.hideModal('profileModal');
        });

        // Close modals when clicking outside
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.classList.remove('active');
                }
            });
        });

        // Route card clicks
        document.querySelectorAll('.route-card').forEach(card => {
            card.addEventListener('click', () => {
                this.selectRoute(card.id);
            });
        });
    }

    setDefaultDate() {
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('dateInput').value = today;
    }

    loadFromURL() {
        const urlParams = new URLSearchParams(window.location.search);
        const origin = urlParams.get('origin');
        const school = urlParams.get('school');
        const date = urlParams.get('date');

        if (origin) document.getElementById('originInput').value = origin;
        if (school) document.getElementById('schoolInput').value = school;
        if (date) document.getElementById('dateInput').value = date;

        // Auto-plan route if we have origin and school
        if (origin && school) {
            setTimeout(() => this.planRoute(), 1000);
        }
    }

    async getCurrentLocation() {
        if (!navigator.geolocation) {
            this.showNotification('Geolocation is not supported by this browser.', 'error');
            return;
        }

        try {
            const position = await new Promise((resolve, reject) => {
                navigator.geolocation.getCurrentPosition(resolve, reject, {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 60000
                });
            });

            const { latitude, longitude } = position.coords;
            document.getElementById('originInput').value = `${latitude.toFixed(6)},${longitude.toFixed(6)}`;
            
            // Update map view to current location
            this.map.setView([latitude, longitude], 15);
            
            this.showNotification('Location updated successfully!', 'success');
        } catch (error) {
            this.showNotification('Unable to get your location. Please enter manually.', 'error');
        }
    }

    async planRoute() {
        const origin = document.getElementById('originInput').value.trim();
        const school = document.getElementById('schoolInput').value;
        const date = document.getElementById('dateInput').value;
        const time = document.getElementById('timeInput').value;
        
        console.log('Planning route with:', { origin, school, date, time });

        if (!origin || origin.trim() === '') {
            this.showNotification('Please enter a starting point.', 'error');
            return;
        }

        if (!school) {
            this.showNotification('Please select a school.', 'error');
            return;
        }

        this.showLoading(true);

        try {
            // Origin can now be either place name or coordinates - let the backend handle it

            // Build API URL
            const params = new URLSearchParams({
                origin: origin,
                school: school
            });
            
            if (date) params.append('date_str', date);

            const response = await fetch(`/api/route?${params}`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log('Route data received:', data);
            this.displayResults(data);
            this.showResults();
            this.showNotification('Route planned successfully!', 'success');
            
        } catch (error) {
            console.error('Error planning route:', error);
            const errorMessage = error.message || 'Failed to plan route. Please try again.';
            this.showNotification(errorMessage, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    displayResults(data) {
        this.currentRoute = data;
        
        // Clear existing layers
        this.clearMap();
        
        // Add markers and routes to map
        this.addMarkersToMap(data);
        this.addRoutesToMap(data);
        
        // Update route cards with real data
        this.updateRouteCards(data);
        
        // Fit map to show all routes
        this.fitMapToRoutes();
    }

    clearMap() {
        // Remove existing layers
        Object.values(this.routeLayers).forEach(layer => {
            if (layer && this.map.hasLayer(layer)) {
                this.map.removeLayer(layer);
            }
        });
        
        // Clear markers
        this.markers.forEach(marker => this.map.removeLayer(marker));
        this.markers = [];
        
        // Reset layers
        this.routeLayers = { fast: null, safe: null, bus: null };
    }

    addMarkersToMap(data) {
        // Origin marker
        const originMarker = L.marker([data.origin.lat, data.origin.lon], {
            icon: L.divIcon({
                className: 'custom-marker origin',
                html: '<i class="fas fa-map-marker-alt"></i>',
                iconSize: [30, 30]
            })
        }).addTo(this.map);
        originMarker.bindTooltip('Starting Point');
        this.markers.push(originMarker);

        // Destination marker
        const destMarker = L.marker([data.destination.lat, data.destination.lon], {
            icon: L.divIcon({
                className: 'custom-marker destination',
                html: '<i class="fas fa-graduation-cap"></i>',
                iconSize: [30, 30]
            })
        }).addTo(this.map);
        destMarker.bindTooltip(data.destination.name || 'School');
        this.markers.push(destMarker);

        // Add bus stops if available
        if (data.bus && data.bus.fastest) {
            const busMarker = L.marker([data.bus.fastest.start_lat, data.bus.fastest.start_lon], {
                icon: L.divIcon({
                    className: 'custom-marker bus',
                    html: '<i class="fas fa-bus"></i>',
                    iconSize: [25, 25]
                })
            }).addTo(this.map);
            busMarker.bindTooltip(`Bus Stop: ${data.bus.fastest.start_label}`);
            this.markers.push(busMarker);
        }
    }

    addRoutesToMap(data) {
        // Use GeoJSON data for realistic routes
        if (data.geojson && data.geojson.features) {
            data.geojson.features.forEach(feature => {
                if (feature.geometry.type === 'LineString') {
                    const coords = feature.geometry.coordinates.map(coord => [coord[1], coord[0]]);
                    const properties = feature.properties;
                    
                    let color = '#3b82f6'; // default blue
                    let weight = 4;
                    let opacity = 0.8;
                    let dashArray = null;
                    
                    if (properties.mode === 'walk') {
                        if (properties.variant === 'fast') {
                            color = '#3b82f6'; // blue
                        } else if (properties.variant === 'safe') {
                            color = '#10b981'; // green
                        } else if (properties.variant === 'to_bus' || properties.variant === 'from_bus') {
                            color = '#8b5cf6'; // purple for walking to/from bus
                        }
                    } else if (properties.mode === 'bus') {
                        color = '#f59e0b'; // orange
                        dashArray = '10, 5';
                    }
                    
                    const polyline = L.polyline(coords, {
                        color: color,
                        weight: weight,
                        opacity: opacity,
                        dashArray: dashArray
                    }).addTo(this.map);
                    
                    // Store the layer for later removal
                    if (properties.mode === 'walk' && properties.variant === 'fast') {
                        this.routeLayers.fast = polyline;
                    } else if (properties.mode === 'walk' && properties.variant === 'safe') {
                        this.routeLayers.safe = polyline;
                    } else if (properties.mode === 'bus') {
                        this.routeLayers.bus = polyline;
                    }
                }
            });
        } else {
            // Fallback to simple routes if no GeoJSON
            if (data.walk) {
                // Fast route
                if (data.walk.fastest && data.walk.fastest.coords) {
                    this.routeLayers.fast = L.polyline(data.walk.fastest.coords, {
                        color: '#1f77b4',
                        weight: 5,
                        opacity: 0.8
                    }).addTo(this.map);
                }

                // Safe route
                if (data.walk.safest && data.walk.safest.coords) {
                    this.routeLayers.safe = L.polyline(data.walk.safest.coords, {
                        color: '#2ca02c',
                        weight: 5,
                        opacity: 0.8
                    }).addTo(this.map);
                }
            }

            // Add bus route if available
            if (data.bus && data.bus.fastest) {
                // Create a simple bus route line (in real app, this would be more complex)
                const busCoords = [
                    [data.origin.lat, data.origin.lon],
                    [data.bus.fastest.start_lat, data.bus.fastest.start_lon],
                    [data.destination.lat, data.destination.lon]
                ];
                
                this.routeLayers.bus = L.polyline(busCoords, {
                    color: '#ff7f0e',
                    weight: 6,
                    opacity: 0.8,
                    dashArray: '10, 5'
                }).addTo(this.map);
            }
        }
    }

    updateRouteCards(data) {
        // Update recommended route (bus if available, otherwise safe walk)
        const recommendedCard = document.getElementById('recommendedRoute');
        if (data.bus && data.bus.fastest) {
            // Bus route
            recommendedCard.querySelector('.route-mode').textContent = 'Bus + Walk';
            recommendedCard.querySelector('.time').textContent = `${data.bus.fastest.total_minutes_fast.toFixed(0)} min`;
            recommendedCard.querySelector('.safety-score').textContent = `Safety: ${data.bus.safest ? data.bus.safest.bus_safety_used.toFixed(0) : 92}%`;
            
            const steps = recommendedCard.querySelectorAll('.route-step');
            steps[0].innerHTML = `<i class="fas fa-walking"></i><span>Walk ${data.bus.fastest.w_fast_min.toFixed(0)} min to bus stop</span>`;
            steps[1].innerHTML = `<i class="fas fa-bus"></i><span>Bus ${data.bus.fastest.bus_min.toFixed(0)} min to school</span>`;
            steps[2].innerHTML = `<i class="fas fa-walking"></i><span>Walk to school entrance</span>`;
        } else {
            // Safe walk route
            recommendedCard.querySelector('.route-mode').textContent = 'Safe Walk';
            recommendedCard.querySelector('.time').textContent = `${data.walk.safest.minutes} min`;
            recommendedCard.querySelector('.safety-score').textContent = `Safety: ${data.walk.safest.safety}%`;
            
            const steps = recommendedCard.querySelectorAll('.route-step');
            steps[0].innerHTML = `<i class="fas fa-walking"></i><span>Walk ${data.walk.safest.minutes} min via safe streets</span>`;
            steps[1].style.display = 'none';
            steps[2].style.display = 'none';
        }

        // Update walking route
        const walkingCard = document.getElementById('walkingRoute');
        walkingCard.querySelector('.time').textContent = `${data.walk.safest.minutes} min`;
        walkingCard.querySelector('.safety-score').textContent = `Safety: ${data.walk.safest.safety}%`;

        // Update fastest route
        const fastestCard = document.getElementById('fastRoute');
        fastestCard.querySelector('.time').textContent = `${data.walk.fastest.minutes} min`;
        fastestCard.querySelector('.safety-score').textContent = `Safety: ${data.walk.fastest.safety}%`;
    }

    fitMapToRoutes() {
        if (this.markers.length > 0) {
            const group = new L.featureGroup(this.markers);
            this.map.fitBounds(group.getBounds().pad(0.1));
        }
    }

    selectRoute(routeId) {
        // Highlight selected route
        document.querySelectorAll('.route-card').forEach(card => {
            card.classList.remove('selected');
        });
        document.getElementById(routeId).classList.add('selected');

        // Show route details or navigate
        this.showRouteDetails(routeId);
    }

    showRouteDetails(routeId) {
        // In a real app, this would show detailed route information
        console.log('Selected route:', routeId);
        
        // For demo purposes, show a notification
        const routeNames = {
            'recommendedRoute': 'Recommended Route',
            'walkingRoute': 'Walking Route',
            'fastRoute': 'Fastest Route'
        };
        
        this.showNotification(`Selected: ${routeNames[routeId]}`, 'info');
    }

    showPlanner() {
        document.getElementById('tripPlanner').style.display = 'block';
        document.getElementById('results').style.display = 'none';
    }

    showResults() {
        document.getElementById('tripPlanner').style.display = 'none';
        document.getElementById('results').style.display = 'block';
    }

    showModal(modalId) {
        document.getElementById(modalId).classList.add('active');
    }

    hideModal(modalId) {
        document.getElementById(modalId).classList.remove('active');
    }

    showLoading(show) {
        const overlay = document.getElementById('loadingOverlay');
        if (show) {
            overlay.classList.add('active');
        } else {
            overlay.classList.remove('active');
        }
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${this.getNotificationIcon(type)}"></i>
            <span>${message}</span>
            <button class="notification-close">
                <i class="fas fa-times"></i>
            </button>
        `;

        // Add styles
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${this.getNotificationColor(type)};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            z-index: 4000;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            max-width: 400px;
            animation: slideInRight 0.3s ease;
        `;

        // Add to page
        document.body.appendChild(notification);

        // Close button functionality
        notification.querySelector('.notification-close').addEventListener('click', () => {
            notification.remove();
        });

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.style.animation = 'slideOutRight 0.3s ease';
                setTimeout(() => notification.remove(), 300);
            }
        }, 5000);
    }

    getNotificationIcon(type) {
        const icons = {
            success: 'check-circle',
            error: 'exclamation-circle',
            warning: 'exclamation-triangle',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    }

    getNotificationColor(type) {
        const colors = {
            success: '#10b981',
            error: '#ef4444',
            warning: '#f59e0b',
            info: '#3b82f6'
        };
        return colors[type] || '#3b82f6';
    }
}

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .custom-marker {
        background: none;
        border: none;
    }
    
    .custom-marker.origin {
        color: #2563eb;
        font-size: 30px;
    }
    
    .custom-marker.destination {
        color: #dc2626;
        font-size: 30px;
    }
    
    .custom-marker.bus {
        color: #f59e0b;
        font-size: 25px;
    }
    
    .route-card.selected {
        border-color: #2563eb;
        background: rgba(37, 99, 235, 0.05);
    }
`;
document.head.appendChild(style);

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new TrustTrackApp();
});
