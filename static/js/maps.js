// Google Maps functionality for the portfolio website

let map;
let markers = [];
let infoWindow;

function initializeMap(projects) {
    // Initialize the map
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 45.0, lng: 10.0 }, // Default center
        zoom: 3,
        styles: [
            {
                "elementType": "geometry",
                "stylers": [{"color": "#212121"}]
            },
            {
                "elementType": "labels.icon",
                "stylers": [{"visibility": "off"}]
            },
            {
                "elementType": "labels.text.fill",
                "stylers": [{"color": "#757575"}]
            },
            {
                "elementType": "labels.text.stroke",
                "stylers": [{"color": "#212121"}]
            },
            {
                "featureType": "administrative",
                "elementType": "geometry",
                "stylers": [{"color": "#757575"}]
            },
            {
                "featureType": "administrative.country",
                "elementType": "labels.text.fill",
                "stylers": [{"color": "#9e9e9e"}]
            }
        ]
    });

    // Initialize info window
    infoWindow = new google.maps.InfoWindow();

    // Add markers for each project
    addProjectMarkers(projects);
    
    // Fit map to show all markers
    fitMapToMarkers();
}

function addProjectMarkers(projects) {
    // Clear existing markers
    clearMarkers();
    
    projects.forEach(project => {
        const marker = new google.maps.Marker({
            position: { lat: project.lat, lng: project.lng },
            map: map,
            title: project.title,
            icon: {
                url: project.type === 'Construction' ? 
                    'https://maps.google.com/mapfiles/ms/icons/yellow-dot.png' : 
                    'https://maps.google.com/mapfiles/ms/icons/green-dot.png',
                scaledSize: new google.maps.Size(32, 32)
            }
        });

        // Create info window content
        const infoContent = `
            <div class="map-info-window">
                <img src="${project.images[0]}" alt="${project.title}">
                <h6>${project.title}</h6>
                <p class="mb-2">${project.location}</p>
                <p class="mb-2"><small>${project.description.substring(0, 100)}...</small></p>
                <div class="mb-2">
                    <span class="badge bg-${project.type === 'Construction' ? 'warning' : 'success'}">${project.type}</span>
                    <span class="badge bg-${project.status === 'Completed' ? 'success' : 'info'} ms-1">${project.status}</span>
                </div>
                <div class="text-center">
                    <button class="btn btn-sm btn-info" onclick="showProjectModal(${project.id})">
                        <i class="fas fa-eye me-1"></i>Quick View
                    </button>
                    <a href="/project/${project.id}" class="btn btn-sm btn-outline-info ms-1">
                        <i class="fas fa-external-link-alt me-1"></i>Full Details
                    </a>
                </div>
            </div>
        `;

        // Add click listener to marker
        marker.addListener('click', () => {
            infoWindow.setContent(infoContent);
            infoWindow.open(map, marker);
            
            // Highlight corresponding project in sidebar
            highlightProjectInSidebar(project.id);
        });

        markers.push(marker);
    });
}

function clearMarkers() {
    markers.forEach(marker => {
        marker.setMap(null);
    });
    markers = [];
}

function fitMapToMarkers() {
    if (markers.length === 0) return;
    
    const bounds = new google.maps.LatLngBounds();
    markers.forEach(marker => {
        bounds.extend(marker.getPosition());
    });
    map.fitBounds(bounds);
    
    // Prevent over-zooming for single marker
    if (markers.length === 1) {
        map.setZoom(10);
    }
}

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

function filterProjects(filter) {
    const projectItems = document.querySelectorAll('.project-item');
    const visibleProjects = [];
    
    projectItems.forEach(item => {
        const projectType = item.getAttribute('data-type');
        
        if (filter === 'all' || projectType === filter) {
            item.style.display = 'block';
            const projectId = parseInt(item.getAttribute('data-project-id'));
            const lat = parseFloat(item.getAttribute('data-lat'));
            const lng = parseFloat(item.getAttribute('data-lng'));
            
            // Find the project data
            fetch('/api/projects')
                .then(response => response.json())
                .then(projects => {
                    const project = projects.find(p => p.id === projectId);
                    if (project) {
                        visibleProjects.push(project);
                    }
                    
                    // Update markers after all projects are processed
                    if (visibleProjects.length === document.querySelectorAll('.project-item[style="display: block;"]').length) {
                        updateMapMarkers(visibleProjects);
                    }
                });
        } else {
            item.style.display = 'none';
        }
    });
}

function updateMapMarkers(projects) {
    // Clear existing markers
    clearMarkers();
    
    // Add markers for filtered projects
    addProjectMarkers(projects);
    
    // Fit map to new markers
    fitMapToMarkers();
}

function initializeProjectList() {
    const projectItems = document.querySelectorAll('.project-item');
    
    projectItems.forEach(item => {
        item.addEventListener('click', function() {
            const projectId = parseInt(this.getAttribute('data-project-id'));
            const lat = parseFloat(this.getAttribute('data-lat'));
            const lng = parseFloat(this.getAttribute('data-lng'));
            
            // Center map on project location
            map.setCenter({ lat: lat, lng: lng });
            map.setZoom(12);
            
            // Find and trigger marker click
            const marker = markers.find(m => {
                const pos = m.getPosition();
                return Math.abs(pos.lat() - lat) < 0.001 && Math.abs(pos.lng() - lng) < 0.001;
            });
            
            if (marker) {
                google.maps.event.trigger(marker, 'click');
            }
        });
    });
}

// Handle window resize
window.addEventListener('resize', function() {
    if (map) {
        google.maps.event.trigger(map, 'resize');
        fitMapToMarkers();
    }
});
