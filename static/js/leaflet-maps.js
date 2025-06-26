// Leaflet.js functionality for OpenStreetMap integration

function initializeLeafletMap(project) {
    // Initialize Leaflet map
    const leafletMap = L.map('leaflet-map').setView([project.lat, project.lng], 15);
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19
    }).addTo(leafletMap);
    
    // Create custom icon based on project type
    const iconUrl = project.type === 'Construction' ? 
        'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-yellow.png' :
        'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png';
    
    const customIcon = L.icon({
        iconUrl: iconUrl,
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
    });
    
    // Add marker with popup
    const marker = L.marker([project.lat, project.lng], { icon: customIcon })
        .addTo(leafletMap)
        .bindPopup(`
            <div class="leaflet-popup-content">
                <h6>${project.title}</h6>
                <p><strong>Location:</strong> ${project.location}</p>
                <p><strong>Type:</strong> ${project.type}</p>
                <p><strong>Status:</strong> ${project.status}</p>
                <img src="${project.images[0]}" alt="${project.title}" 
                     style="width: 100%; max-width: 200px; height: auto; border-radius: 4px; margin-top: 8px;">
            </div>
        `);
    
    // Open popup by default
    marker.openPopup();
    
    // Add scale control
    L.control.scale().addTo(leafletMap);
    
    // Add additional map layers
    const satellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
    });
    
    const terrain = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
    });
    
    // Layer control
    const baseMaps = {
        "OpenStreetMap": L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }),
        "Satellite": satellite,
        "Terrain": terrain
    };
    
    L.control.layers(baseMaps).addTo(leafletMap);
    
    // Add fullscreen control if available
    if (L.control.fullscreen) {
        leafletMap.addControl(new L.control.fullscreen());
    }
    
    return leafletMap;
}

// Global variables for homepage map
let homepageMap;
let homepageMarkers = [];

// Function to create a multi-project Leaflet map
function initializeMultiProjectLeafletMap(projects, containerId) {
    homepageMap = L.map(containerId).setView([45.0, 10.0], 3);
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19
    }).addTo(homepageMap);
    
    // Add markers for each project
    addHomepageMarkers(projects);
    
    // Fit map to show all markers
    fitHomepageMapToMarkers();
    
    // Add scale control
    L.control.scale().addTo(homepageMap);
    
    return homepageMap;
}

// Function to add markers to homepage map
function addHomepageMarkers(projects) {
    // Clear existing markers
    clearHomepageMarkers();
    
    projects.forEach(project => {
        const iconUrl = project.type === 'Construction' ? 
            'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-yellow.png' :
            'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png';
        
        const customIcon = L.icon({
            iconUrl: iconUrl,
            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41]
        });
        
        const marker = L.marker([project.lat, project.lng], { icon: customIcon })
            .addTo(homepageMap)
            .bindPopup(`
                <div class="leaflet-popup-content">
                    <img src="${project.images[0]}" alt="${project.title}" 
                         style="width: 100%; max-width: 200px; height: 120px; object-fit: cover; border-radius: 4px; margin-bottom: 8px;">
                    <h6>${project.title}</h6>
                    <p class="mb-1"><strong>Location:</strong> ${project.location}</p>
                    <p class="mb-1"><strong>Type:</strong> ${project.type}</p>
                    <p class="mb-2"><strong>Status:</strong> ${project.status}</p>
                    <p class="mb-2" style="font-size: 0.9em;">${project.description.substring(0, 100)}...</p>
                    <div style="margin-top: 10px;">
                        <button class="btn btn-sm btn-info" onclick="showProjectModal('${project.id}')">
                            Quick View
                        </button>
                        <a href="/project/${project.id}" class="btn btn-sm btn-outline-info ms-1">
                            Full Details
                        </a>
                    </div>
                </div>
            `);
        
        // Add click event to highlight sidebar item
        marker.on('click', function() {
            highlightProjectInSidebar(project.id);
        });
        
        homepageMarkers.push(marker);
    });
}

// Function to clear homepage markers
function clearHomepageMarkers() {
    homepageMarkers.forEach(marker => {
        homepageMap.removeLayer(marker);
    });
    homepageMarkers = [];
}

// Function to fit map to markers
function fitHomepageMapToMarkers() {
    if (homepageMarkers.length > 0) {
        const group = new L.featureGroup(homepageMarkers);
        homepageMap.fitBounds(group.getBounds().pad(0.1));
    }
}

// Function to highlight project in sidebar
function highlightProjectInSidebar(projectId) {
    // Remove previous highlights
    document.querySelectorAll('.project-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Highlight current project
    const projectItem = document.querySelector(`[data-project-id="${projectId}"]`);
    if (projectItem) {
        projectItem.classList.add('active');
        projectItem.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

// Function to show project modal
function showProjectModal(projectId) {
    fetch(`/api/project/${projectId}`)
        .then(response => response.json())
        .then(project => {
            // Populate modal with project data
            const modal = document.getElementById('projectModal');
            const modalTitle = modal.querySelector('.modal-title');
            const modalImage = modal.querySelector('#modal-image');
            const modalDescription = modal.querySelector('#modal-description');
            const modalDetails = modal.querySelector('#modal-details');
            const modalViewDetails = modal.querySelector('#modal-view-details');
            
            modalTitle.textContent = project.title;
            modalImage.src = project.images[0];
            modalImage.alt = project.title;
            modalDescription.textContent = project.description;
            modalViewDetails.href = `/project/${project.id}`;
            
            // Populate details list
            modalDetails.innerHTML = '';
            const details = [
                `Duration: ${project.details.duration}`,
                `Team Size: ${project.details.team_size}`,
                `Area: ${project.details.area}`,
                `Status: ${project.status}`
            ];
            
            details.forEach(detail => {
                const li = document.createElement('li');
                li.textContent = detail;
                modalDetails.appendChild(li);
            });
            
            // Show modal
            const bootstrapModal = new bootstrap.Modal(modal);
            bootstrapModal.show();
        })
        .catch(error => {
            console.error('Error fetching project data:', error);
        });
}

// Function to initialize filters
function initializeFilters() {
    const filterButtons = document.querySelectorAll('[data-filter]');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const filter = this.getAttribute('data-filter');
            
            // Update active button
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Filter projects
            filterProjects(filter);
        });
    });
}

// Function to filter projects
function filterProjects(filter) {
    const projectItems = document.querySelectorAll('.project-item');
    const visibleProjects = [];
    
    projectItems.forEach(item => {
        const projectType = item.getAttribute('data-type');
        
        if (filter === 'all' || projectType === filter) {
            item.style.display = 'block';
            const projectId = parseInt(item.getAttribute('data-project-id'));
            
            // Find the project data
            fetch('/api/projects')
                .then(response => response.json())
                .then(projects => {
                    const project = projects.find(p => p.id === projectId);
                    if (project) {
                        visibleProjects.push(project);
                    }
                    
                    // Update markers after all visible projects are collected
                    if (visibleProjects.length === document.querySelectorAll('.project-item[style="display: block;"]').length) {
                        updateHomepageMapMarkers(visibleProjects);
                    }
                });
        } else {
            item.style.display = 'none';
        }
    });
}

// Function to update map markers
function updateHomepageMapMarkers(projects) {
    // Clear existing markers
    clearHomepageMarkers();
    
    // Add markers for filtered projects
    addHomepageMarkers(projects);
    
    // Fit map to new markers
    fitHomepageMapToMarkers();
}

// Function to initialize project list interactions
function initializeProjectList() {
    const projectItems = document.querySelectorAll('.project-item');
    
    projectItems.forEach(item => {
        item.addEventListener('click', function() {
            const projectId = parseInt(this.getAttribute('data-project-id'));
            const lat = parseFloat(this.getAttribute('data-lat'));
            const lng = parseFloat(this.getAttribute('data-lng'));
            
            // Center map on project location
            homepageMap.setView([lat, lng], 12);
            
            // Find and open marker popup
            const marker = homepageMarkers.find(m => {
                const pos = m.getLatLng();
                return Math.abs(pos.lat - lat) < 0.001 && Math.abs(pos.lng - lng) < 0.001;
            });
            
            if (marker) {
                marker.openPopup();
            }
            
            // Highlight this project
            highlightProjectInSidebar(projectId);
        });
    });
}

// Utility function to add custom controls to Leaflet maps
function addCustomControls(map) {
    // Custom info control
    const info = L.control({ position: 'topright' });
    
    info.onAdd = function(map) {
        this._div = L.DomUtil.create('div', 'leaflet-control leaflet-control-custom');
        this._div.innerHTML = '<h4>Project Locations</h4>Click on markers to view project details';
        this._div.style.backgroundColor = 'rgba(0,0,0,0.8)';
        this._div.style.color = 'white';
        this._div.style.padding = '10px';
        this._div.style.borderRadius = '5px';
        return this._div;
    };
    
    info.addTo(map);
    
    return info;
}

// Function to handle map interactions
function setupMapInteractions(map, projects) {
    // Add click handler for map
    map.on('click', function(event) {
        console.log('Map clicked at:', event.latlng);
    });
    
    // Add zoom end handler
    map.on('zoomend', function() {
        console.log('Current zoom level:', map.getZoom());
    });
    
    // Add move end handler
    map.on('moveend', function() {
        console.log('Map center:', map.getCenter());
    });
}

// Export functions for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initializeLeafletMap,
        initializeMultiProjectLeafletMap,
        addCustomControls,
        setupMapInteractions
    };
}
